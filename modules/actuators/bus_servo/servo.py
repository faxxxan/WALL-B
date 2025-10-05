#!/usr/bin/env python

import sys
import os
import select
import time

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
        
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# sys.path.append("..")
# Uses STServo and SCServo SDK library
from modules.actuators.bus_servo.STservo_sdk import *
from modules.actuators.bus_servo.SCservo_sdk import *

from modules.base_module import BaseModule

# Control table address
ADDR_TORQUE_ENABLE         = 40 # Same address for both ST and SC servos
ADDR_SCS_GOAL_ACC          = 41
ADDR_SCS_GOAL_POSITION     = 42 # Used in SCServo move
ADDR_SCS_GOAL_SPEED        = 46
ADDR_SCS_PRESENT_POSITION  = 56


class Servo(BaseModule):
    def __init__(self, **kwargs):
        """
        Servo class
        """
        
        self.identifier = kwargs.get('name')
        self.model = kwargs.get('model', 'ST')
        self.index = kwargs.get('id')
        self.range = kwargs.get('range')
        self.start = kwargs.get('start') # Default start position
        self.poses = kwargs.get('poses')  # Dictionary of poses
        self.baudrate = kwargs.get('baudrate', 1000000)
        self.port = kwargs.get('port', '/dev/ttyACM0') # Change as needed, find with `ls /dev/ttyACM*`
        self.calibrate_on_boot = kwargs.get('calibrate_on_boot', True) # Loop to show position for manual configuration
        self.demonstrate_on_boot = kwargs.get('demonstrate_on_boot', False) # Move to min and max to demonstrate range
        self.pos = self.start
        self.speed = 2400 # 3073
        self.acceleration = 50
        
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.portHandler = PortHandler(self.port)
        
        # if model starts with ST or SC, use the appropriate packet handler
        if self.model.startswith('ST'):
            self.packetHandler = sts(self.portHandler)
        elif self.model.startswith('SC'):
            self.packetHandler = PacketHandler(1) # 1 = protocol_end in examples
        else:
            raise ValueError(f"Unknown servo model: {self.model}. Supported models are ST and SC.")

        # Open port
        if not self.portHandler.openPort():
            raise Exception("Failed to open the port")

        # Set port baudrate
        if not self.portHandler.setBaudRate(self.baudrate):
            raise Exception("Failed to change the baudrate")
        
    
    def exit(self):
        # Detach servo
        if self.model.startswith('ST'):
            # Disable torque for STServo
            sts_comm_result, sts_error = self.packetHandler.write1ByteTxRx(self.index, ADDR_TORQUE_ENABLE, 0)
            if not self.handle_errors(sts_comm_result, sts_error):
                self.log(f"ST Servo {self.identifier} disabled")
        else:
            # Disable torque for SCServo
            scs_comm_result, scs_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.index, ADDR_TORQUE_ENABLE, 0)
            if not self.handle_errors(scs_comm_result, scs_error):
                self.log(f"SC Servo {self.identifier} disabled")
    
        self.portHandler.closePort()

    def setup_messaging(self):
        self.subscribe('servo:' + self.identifier + ':mvabs', self.move)
        self.subscribe('servo:' + self.identifier + ':mv', self.move_relative)
        self.subscribe('system/exit', self.exit)
        
        if self.calibrate_on_boot:
            self.calibrate_dynamic() # Log will show current position repeatedly to help with manual configuration
        
        self.pos = self.get_position()  # Get initial position to avoid jumping from unknown position
        
        if self.demonstrate_on_boot:
            self.log(f"Demonstrating servo {self.identifier} movement")
            if self.range is not None:
                self.move(self.range[0])
                time.sleep(1)
                self.move(self.range[1])
                time.sleep(1)
            else:
                self.log(f"Range not set for servo {self.identifier}, cannot demonstrate movement", level='warning')
        
        # Move to start position
        # if self.get_pose_value('stand') is not None:
            # self.start = self.get_pose_value('stand')
        self.move(self.start)
        
    def move(self, position):
        """
        Move the servo to an absolute position.
        :param position: Position to move to (0-100)
        """
        if position < self.range[0] or position > self.range[1]:
            self.log(f"Position {position} out of range ({self.range[0]}-{self.range[1]})", level='error')
            return
        
        # Write STServo goal position
        if self.model.startswith('ST'):
            sts_comm_result, sts_error = self.packetHandler.WritePosEx(self.index, position, self.speed, self.acceleration)
            if not self.handle_errors(sts_comm_result, sts_error):
                self.log(f"Moved servo {self.identifier} from {self.pos} to position {position}")
                self.pos = position  # Update current position
        elif self.model.startswith('SC'):
            self.packetHandler.write1ByteTxRx(self.portHandler, self.index, ADDR_SCS_GOAL_ACC, self.acceleration)
            self.packetHandler.write2ByteTxRx(self.portHandler, self.index, ADDR_SCS_GOAL_SPEED, self.speed)
            self.packetHandler.write2ByteTxRx(self.portHandler, self.index, ADDR_SCS_GOAL_POSITION, position)
            self.log(f"Moved servo {self.identifier} from {self.pos} to position {position}")
    
    def move_relative(self, delta):
        """
        Move the servo relative to its current position.
        :param delta: Change in position (can be negative)
        """
        new_position = self.pos + delta
        if new_position < self.range[0] or new_position > self.range[1]:
            self.log(f"Position {new_position} out of range ({self.range[0]}-{self.range[1]})", level='error')
            return
        
        # Move to new position
        self.move(new_position)
        
    def get_position(self):
        """
        Get the current position of the servo.
        """
        if self.model.startswith('ST'):
            # Read STServo present position
            sts_present_position, sts_present_speed, sts_comm_result, sts_error = self.packetHandler.ReadPosSpeed(self.index)
            if not self.handle_errors(sts_comm_result, sts_error):
                # self.log("[ID:%03d] PresPos:%d PresSpd:%d" % (self.index, sts_present_position, sts_present_speed))
                return sts_present_position
        else:
            return self.sc_get_position_speed('position')
    
    def get_speed(self):
        """
        Get the current speed of the servo.
        """
        if self.model.startswith('ST'):
            # Read STServo present position
            sts_present_position, sts_present_speed, sts_comm_result, sts_error = self.packetHandler.ReadPosSpeed(self.index)
            if not self.handle_errors(sts_comm_result, sts_error):
                return sts_present_speed
        else:
            return self.sc_get_position_speed('speed')
        
        
    def sc_get_position_speed(self, pos_or_speed):
        # Read SCServo present position
        scs_present_position_speed, scs_comm_result, scs_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.index, ADDR_SCS_PRESENT_POSITION)
        if not self.handle_errors(scs_comm_result, scs_error):
            scs_present_position = SCS_LOWORD(scs_present_position_speed)
            scs_present_speed = SCS_HIWORD(scs_present_position_speed)
            if pos_or_speed == 'position':
                return scs_present_position
            elif pos_or_speed == 'speed':
                return SCS_TOHOST(scs_present_speed, 15)
    
    def enable_continuous(self):
        """
        Set the servo mode.
        :param mode: Mode to set (e.g., 'wheel', 'position')
        """
        if self.model.startswith('SC'):
            raise ValueError("Continuous mode is not supported for SCServo models.")
        sts_comm_result, sts_error = self.packetHandler.WheelMode(self.index)
        if not self.handle_errors(sts_comm_result, sts_error):
            self.log(f"Servo {self.name} set to wheel mode")
            
    def turn_wheel(self, speed):
        if self.model.startswith('SC'):
            raise ValueError("Continuous mode is not supported for SCServo models.")
        sts_comm_result, sts_error = self.packetHandler.WriteSpec(self.index, speed, self.acceleration)
        if not self.handle_errors(sts_comm_result, sts_error):
            self.log(f"Servo {self.name} turned at speed {speed}")
            
    def handle_errors(self, comm_result, error):
        """
        Handle communication errors.
        :param comm_result: Communication result
        :param error: Error code
        """
        if comm_result != COMM_SUCCESS:
            self.log("%s" % self.packetHandler.getTxRxResult(comm_result), level='error')
            # log stack trace for debugging
            return True
        if error != 0:
            self.log("%s" % self.packetHandler.getRxPacketError(error), level='error')
            return True
        return False
    
    def get_pose_value(self, pose_name):
        """
        Returns the position value for the given pose name from self.poses.
        """
        if not self.poses:
            return None
        for pose in self.poses:
            if pose_name in pose:
                return pose[pose_name]
        return None  # or raise an exception if preferred

    def calibrate(self):
        """
        Move each servo to capture min and max positions for calibration.
        """
        self.log(f"Move servo {self.identifier} to minimum position and press any key...")
        getch()  # Waits for a single key press
        min = self.get_position()
        self.log(f"Captured minimum position: {min}")
        self.log(f"Move servo {self.identifier} to maximum position and press any key...")
        getch()  # Waits for a single key press
        max = self.get_position()
        self.log(f"Captured maximum position: {max}")
        self.range = (min, max)
        if self.start is not None and (self.start < min or self.start > max):
            self.start = (min + max) // 2
            self.log(f"Start position {self.start} out of new range, setting to midpoint {self.start}")
        self.log(f"Updated range for {self.identifier}: {self.range}. Start position: {self.start}")

    def calibrate_dynamic(self):
        """
        Continuously log the current position to help with manual calibration.
        Store min an max as they are found.
        Complete on key press. and store in self.range
        """
        self.log(f"Calibrating servo {self.identifier}. Move the servo to find min and max positions. Press any key to finish...")
        min_pos = None
        max_pos = None
        try:
            while True:
                pos = self.get_position()
                if min_pos is None or pos < min_pos:
                    min_pos = pos
                if max_pos is None or pos > max_pos:
                    max_pos = pos
                # Print on the same line, pad with spaces to clear previous content
                print(f"\rCurrent position: {pos}, Min: {min_pos}, Max: {max_pos}      ", end='', flush=True)
                time.sleep(0.05)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.read(1)  # Consume the key so buffer is cleared
                    break
        except KeyboardInterrupt:
            pass
        print()  # Move to next line after loop
        if min_pos is not None and max_pos is not None:
            self.range = (min_pos, max_pos)
            self.log(f"Calibration complete for {self.identifier}. Range: {self.range}")
        else:
            self.log(f"No positions recorded during calibration for {self.identifier}.", level='warning')
            
        if self.start is not None and (self.start < min_pos or self.start > max_pos):
            self.start = (min_pos + max_pos) // 2
            self.log(f"Start position {self.start} out of new range, setting to midpoint {self.start}")







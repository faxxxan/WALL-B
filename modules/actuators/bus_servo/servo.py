#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available STServo model on this example : All models using Protocol STS
# This example is tested with a STServo and an URT
#

import sys
import os

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

sys.path.append("..")
# Uses STServo SDK library
from STservo_sdk import *

from modules.base_module import BaseModule

class Servo(BaseModule):
    def __init__(self, **kwargs):
        """
        Servo class
        """
        
        self.identifier = kwargs.get('name')
        self.index = kwargs.get('id')
        self.range = kwargs.get('range')
        self.start = kwargs.get('start', 50)
        self.baudrate = kwargs.get('baudrate', 1000000)
        self.port = kwargs.get('port', '/dev/ttyACM0')
        self.pos = self.start
        self.speed = 2400
        self.acceleration = 50
        
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.portHandler = PortHandler(self.port)

        # Initialize PacketHandler instance
        # Get methods and members of Protocol
        self.packetHandler = sts(self.portHandler)
        
        # Open port
        if not self.portHandler.openPort():
            raise Exception("Failed to open the port")

        # Set port baudrate
        if not self.portHandler.setBaudRate(self.baudrate):
            raise Exception("Failed to change the baudrate")
    
    def exit(self):
        self.portHandler.closePort()

    def setup_messaging(self):
        self.subscribe('servo:' + self.identifier + ':mvabs', self.move)
        self.subscribe('servo:' + self.identifier + ':mv', self.move_relative)
        
        self.pos = self.get_position()  # Get initial position to avoid jumping from unknown position
        # Move to start position
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
        # Write STServo goal position/moving speed/moving acc
        sts_comm_result, sts_error = self.packetHandler.WritePosEx(self.index, position, self.speed, self.acceleration)
        if not self.handle_errors(sts_comm_result, sts_error):
            self.log(f"Moved servo {self.name} to position {position}")
            self.pos = position  # Update current position
    
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
        # Read STServo present position
        sts_present_position, sts_present_speed, sts_comm_result, sts_error = self.packetHandler.ReadPosSpeed(self.index)
        if not self.handle_errors(sts_comm_result, sts_error):
            self.log("[ID:%03d] PresPos:%d PresSpd:%d" % (STS_ID, sts_present_position, sts_present_speed))
            return sts_present_position
    
    def get_speed(self):
        """
        Get the current speed of the servo.
        """
        # Read STServo present position
        sts_present_position, sts_present_speed, sts_comm_result, sts_error = self.packetHandler.ReadPosSpeed(self.index)
        if not self.handle_errors(sts_comm_result, sts_error):
            return sts_present_speed
    
    def enable_continuous(self):
        """
        Set the servo mode.
        :param mode: Mode to set (e.g., 'wheel', 'position')
        """
        sts_comm_result, sts_error = self.packetHandler.WheelMode(self.index)
        if not self.handle_errors(sts_comm_result, sts_error):
            self.log(f"Servo {self.name} set to wheel mode")
            
    def turn_wheel(self, speed):
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
            return True
        if error != 0:
            self.log("%s" % self.packetHandler.getRxPacketError(error), level='error')
            return True
        return False
            
            
            






    


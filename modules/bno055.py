from pubsub import pub
import smbus
from time import sleep
from modules.base_module import BaseModule

# BNO055 Register addresses
BNO055_OPR_MODE_ADDR = 0x3D
BNO055_EULER_H_LSB_ADDR = 0x1A
BNO055_ACCEL_DATA_X_LSB_ADDR = 0x08

class BNO055(BaseModule):
    def __init__(self, **kwargs):
        self.bus = smbus.SMBus(kwargs.get('bus', 1))
        self.name = kwargs.get('name', 'bno055')
        sleep(2)
        self.address = kwargs.get('address', 0x28)
        self.line_offset = kwargs.get('line_offset', 0) # for console output formatting (move up X lines)
        self.test_on_boot = kwargs.get('test_on_boot', False)
        self._init_sensor()
        if self.test_on_boot:
            while True:
                self.read_data()
                
    def setup_messaging(self):
        self.subscribe('bno055/read', self.read_data)
        self.subscribe('bno055/read/euler', self.read_euler)
        self.subscribe('bno055/read/accel', self.read_accel)
        # self.subscribe('system/loop/1', self.read_data)

    def _init_sensor(self):
        # Set to config mode
        try:
            self.bus.write_byte_data(self.address, BNO055_OPR_MODE_ADDR, 0x00)
            sleep(0.025)
            # Set to NDOF mode (fusion)
            self.bus.write_byte_data(self.address, BNO055_OPR_MODE_ADDR, 0x0C)
            sleep(0.02)
        except OSError:
            print("BNO055: I2C communication error during initialization.")

    def _to_signed(self, n):
        return n - 65536 if n > 32767 else n

    def read_euler(self):
        try:
            data = self.bus.read_i2c_block_data(self.address, BNO055_EULER_H_LSB_ADDR, 6)
            heading = (data[1] << 8 | data[0]) / 16.0
            roll = (data[3] << 8 | data[2]) / 16.0
            pitch = (data[5] << 8 | data[4]) / 16.0
            return {'heading': heading, 'roll': roll, 'pitch': pitch}
        except OSError:
            print("BNO055: I2C communication error during Euler read.")
            return None

    def read_accel(self):
        try:
            data = self.bus.read_i2c_block_data(self.address, BNO055_ACCEL_DATA_X_LSB_ADDR, 6)
            x = self._to_signed(data[1] << 8 | data[0]) / 100.0
            y = self._to_signed(data[3] << 8 | data[2]) / 100.0
            z = self._to_signed(data[5] << 8 | data[4]) / 100.0
            return {'x': x, 'y': y, 'z': z}
        except OSError:
            print("BNO055: I2C communication error during Accel read.")
            return None

    def read_data(self):
        euler = self.read_euler()
        accel = self.read_accel()
        if euler is not None and accel is not None:
            # Pad each value for consistent line length
            output = (
                f"Euler: "
                f"H={euler['heading']:7.2f} "
                f"R={euler['roll']:7.2f} "
                f"P={euler['pitch']:7.2f} | "
                f"Accel: "
                f"X={accel['x']:7.2f} "
                f"Y={accel['y']:7.2f} "
                f"Z={accel['z']:7.2f}"
            )
            if self.line_offset > 0:
                print('\033[F', end='')  # Move cursor up one line
                print(f"r{self.name}:{output}") 
            else:
                print(f"\r{self.name}:{output}", end="", flush=True)
        sleep(0.5)

import json
import os
from time import sleep

import smbus

from modules.base_module import BaseModule


class BNO055(BaseModule):
    """Driver for the DFRobot BNO055 9-axis IMU."""

    # Register map (subset required for initialization and data reads)
    _BNO055_CHIP_ID_ADDR = 0x00
    _BNO055_PAGE_ID_ADDR = 0x07
    _BNO055_ACC_DATA_X_LSB_ADDR = 0x08
    _BNO055_MAG_DATA_X_LSB_ADDR = 0x0E
    _BNO055_GYR_DATA_X_LSB_ADDR = 0x14
    _BNO055_EUL_HEADING_LSB_ADDR = 0x1A
    _BNO055_QUA_DATA_W_LSB_ADDR = 0x20
    _BNO055_LIA_DATA_X_LSB_ADDR = 0x28
    _BNO055_GRV_DATA_X_LSB_ADDR = 0x2E
    _BNO055_TEMP_ADDR = 0x34
    _BNO055_CALIB_STAT_ADDR = 0x35
    _BNO055_SYS_STATUS_ADDR = 0x39
    _BNO055_SYS_ERR_ADDR = 0x3A
    _BNO055_UNIT_SEL_ADDR = 0x3B
    _BNO055_OPR_MODE_ADDR = 0x3D
    _BNO055_PWR_MODE_ADDR = 0x3E
    _BNO055_SYS_TRIGGER_ADDR = 0x3F

    _BNO055_ACC_OFFSET_X_LSB_ADDR = 0x55

    _EXPECTED_CHIP_ID = 0xA0

    _POWER_MODES = {
        "NORMAL": 0x00,
        "LOW_POWER": 0x01,
        "SUSPEND": 0x02,
    }

    _OPERATION_MODES = {
        "CONFIG": 0x00,
        "ACCONLY": 0x01,
        "MAGONLY": 0x02,
        "GYROONLY": 0x03,
        "ACCMAG": 0x04,
        "ACCGYRO": 0x05,
        "MAGGYRO": 0x06,
        "AMG": 0x07,
        "IMU": 0x08,
        "COMPASS": 0x09,
        "M4G": 0x0A,
        "NDOF_FMC_OFF": 0x0B,
        "NDOF": 0x0C,
    }

    _VECTOR_SCALES = {
        "ACCEL": 100.0,
        "MAG": 16.0,
        "GYRO": 900.0,
        "EULER": 16.0,
        "LINEAR": 100.0,
        "GRAVITY": 100.0,
    }

    _CALIBRATION_DATA_LENGTH = 22

    def __init__(self, **kwargs):
        """Initialize the BNO055 sensor."""
        self._messaging_service = None
        self.address = kwargs.get("address", 0x28)
        self._name = kwargs.get("name") or f"addr_{self.address:02x}"
        self._operation_mode_name = str(kwargs.get("operation_mode", "NDOF")).upper()
        self._power_mode_name = str(kwargs.get("power_mode", "NORMAL")).upper()
        self._external_crystal = kwargs.get("external_crystal", True)
        self._calibration_file = kwargs.get("calibration_file")
        self._init_delay = kwargs.get("init_delay", 0.65)
        self._retries = kwargs.get("retries", 5)
        self._retry_delay = kwargs.get("retry_delay", 0.1)
        self._debug_on_boot = kwargs.get("debug_on_boot", False)

        units = kwargs.get("units") or {}
        if not isinstance(units, dict):
            units = dict(units)

        self.bus = smbus.SMBus(kwargs.get("bus", 1))

        self._unit_selection = self._compute_unit_selection(units)

        self._ensure_chip_ready()
        self._configure_sensor()
        if self._calibration_file:
            self._try_load_calibration(self._calibration_file)

    def setup_messaging(self):
        """Register messaging topics for interacting with the sensor."""
        base_topics = {
            "read/euler": self._handle_read_euler,
            "read/quaternion": self._handle_read_quaternion,
            "read/gyroscope": self._handle_read_gyroscope,
            "read/acceleration": self._handle_read_acceleration,
            "read/magnetometer": self._handle_read_magnetometer,
            "read/linear": self._handle_read_linear,
            "read/gravity": self._handle_read_gravity,
            "read/temperature": self._handle_read_temperature,
            "status": self._handle_get_status,
            "calibration/status": self._handle_get_calibration_status,
            "calibration/read": self._handle_read_calibration,
        }
        for suffix, handler in base_topics.items():
            self.subscribe(self._topic(suffix), handler)

        self.subscribe(self._topic("set/operation_mode"), self._handle_set_operation_mode)
        self.subscribe(self._topic("set/power_mode"), self._handle_set_power_mode)
        self.subscribe(self._topic("calibration/save"), self._handle_save_calibration)
        self.subscribe(self._topic("calibration/load"), self._handle_load_calibration)

        if self._debug_on_boot:
            self.subscribe('system/loop/1', self._handle_debug_loop)

    def _ensure_chip_ready(self):
        """Block until the chip reports the expected ID."""
        for attempt in range(self._retries):
            try:
                chip_id = self._read_byte(self._BNO055_CHIP_ID_ADDR)
            except OSError:
                sleep(self._retry_delay)
                continue
            if chip_id == self._EXPECTED_CHIP_ID:
                return
            sleep(self._retry_delay)
        raise RuntimeError(f"BNO055 chip ID check failed after {self._retries} attempts")

    def _configure_sensor(self):
        """Apply power, unit, and operation mode settings."""
        self._set_operation_mode("CONFIG")
        sleep(0.02)

        self._write_byte(self._BNO055_PWR_MODE_ADDR, self._POWER_MODES[self._power_mode_name])
        sleep(0.01)

        self._write_byte(self._BNO055_PAGE_ID_ADDR, 0)
        sleep(0.01)

        self._write_byte(self._BNO055_UNIT_SEL_ADDR, self._unit_selection)
        sleep(0.01)

        self._write_byte(self._BNO055_SYS_TRIGGER_ADDR, 0x00)
        sleep(0.01)

        if self._external_crystal:
            # Enable external crystal oscillator when available.
            self._write_byte(self._BNO055_SYS_TRIGGER_ADDR, 0x80)
            sleep(0.05)

        sleep(self._init_delay)
        self._set_operation_mode(self._operation_mode_name)
        sleep(0.05)

    def _set_operation_mode(self, mode_name):
        mode_name = mode_name.upper()
        if mode_name not in self._OPERATION_MODES:
            raise ValueError(f"Unsupported operation mode: {mode_name}")
        self._write_byte(self._BNO055_OPR_MODE_ADDR, self._OPERATION_MODES[mode_name])
        self._operation_mode_name = mode_name

    def set_operation_mode(self, mode_name):
        """Public wrapper to change operation mode at runtime."""
        self._set_operation_mode(mode_name)
        sleep(0.05)

    def set_power_mode(self, mode_name):
        mode_name = mode_name.upper()
        if mode_name not in self._POWER_MODES:
            raise ValueError(f"Unsupported power mode: {mode_name}")
        self._write_byte(self._BNO055_PWR_MODE_ADDR, self._POWER_MODES[mode_name])
        self._power_mode_name = mode_name
        sleep(0.01)

    def read_euler(self):
        """Return heading, roll, and pitch in degrees."""
        data = self._read_vector(self._BNO055_EUL_HEADING_LSB_ADDR, self._VECTOR_SCALES["EULER"])
        return {"heading": data[0], "roll": data[1], "pitch": data[2]}

    def read_quaternion(self):
        raw = self._read_bytes(self._BNO055_QUA_DATA_W_LSB_ADDR, 8)
        w, x, y, z = [self._twos_complement(raw[i] | (raw[i + 1] << 8)) / 16384.0 for i in range(0, 8, 2)]
        return {"w": w, "x": x, "y": y, "z": z}

    def read_gyroscope(self):
        data = self._read_vector(self._BNO055_GYR_DATA_X_LSB_ADDR, self._VECTOR_SCALES["GYRO"])
        return {"x": data[0], "y": data[1], "z": data[2]}

    def read_acceleration(self):
        data = self._read_vector(self._BNO055_ACC_DATA_X_LSB_ADDR, self._VECTOR_SCALES["ACCEL"])
        return {"x": data[0], "y": data[1], "z": data[2]}

    def read_magnetometer(self):
        data = self._read_vector(self._BNO055_MAG_DATA_X_LSB_ADDR, self._VECTOR_SCALES["MAG"])
        return {"x": data[0], "y": data[1], "z": data[2]}

    def read_linear_acceleration(self):
        data = self._read_vector(self._BNO055_LIA_DATA_X_LSB_ADDR, self._VECTOR_SCALES["LINEAR"])
        return {"x": data[0], "y": data[1], "z": data[2]}

    def read_gravity(self):
        data = self._read_vector(self._BNO055_GRV_DATA_X_LSB_ADDR, self._VECTOR_SCALES["GRAVITY"])
        return {"x": data[0], "y": data[1], "z": data[2]}

    def read_temperature(self):
        value = self._read_byte(self._BNO055_TEMP_ADDR)
        return self._signed_byte(value)

    def get_system_status(self):
        status = self._read_byte(self._BNO055_SYS_STATUS_ADDR)
        error = self._read_byte(self._BNO055_SYS_ERR_ADDR)
        return {"status": status, "error": error}

    def get_calibration_status(self):
        value = self._read_byte(self._BNO055_CALIB_STAT_ADDR)
        return {
            "system": (value >> 6) & 0x03,
            "gyroscope": (value >> 4) & 0x03,
            "accelerometer": (value >> 2) & 0x03,
            "magnetometer": value & 0x03,
        }

    def is_fully_calibrated(self):
        status = self.get_calibration_status()
        return all(level == 3 for level in status.values())

    def read_calibration_data(self):
        self._set_operation_mode("CONFIG")
        sleep(0.05)
        data = self._read_bytes(self._BNO055_ACC_OFFSET_X_LSB_ADDR, self._CALIBRATION_DATA_LENGTH)
        self._set_operation_mode(self._operation_mode_name)
        sleep(0.05)
        return list(data)

    def load_calibration_data(self, calibration_bytes):
        if len(calibration_bytes) != self._CALIBRATION_DATA_LENGTH:
            raise ValueError("Calibration data must be 22 bytes long")
        self._set_operation_mode("CONFIG")
        sleep(0.05)
        self._write_bytes(self._BNO055_ACC_OFFSET_X_LSB_ADDR, calibration_bytes)
        sleep(0.05)
        self._set_operation_mode(self._operation_mode_name)
        sleep(0.05)

    def save_calibration_to_file(self, filepath):
        data = self.read_calibration_data()
        with open(filepath, "w", encoding="utf-8") as handle:
            json.dump({"calibration": data}, handle, indent=2)

    def load_calibration_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.load_calibration_data(payload["calibration"])

    def _try_load_calibration(self, filepath):
        if not os.path.exists(filepath):
            self._safe_log(f"Calibration file not found: {filepath}", level="debug")
            return
        try:
            self.load_calibration_from_file(filepath)
            self._safe_log(f"Loaded calibration data from {filepath}", level="info")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self._safe_log(f"Failed to load calibration data: {exc}", level="warning")

    def _handle_read_euler(self, reply_topic=None, **unused):
        data = self.read_euler()
        return self._publish_response("data/euler", {"source": self._name, "euler": data}, reply_topic)

    def _handle_read_quaternion(self, reply_topic=None, **unused):
        data = self.read_quaternion()
        return self._publish_response("data/quaternion", {"source": self._name, "quaternion": data}, reply_topic)

    def _handle_read_gyroscope(self, reply_topic=None, **unused):
        data = self.read_gyroscope()
        return self._publish_response("data/gyroscope", {"source": self._name, "gyroscope": data}, reply_topic)

    def _handle_read_acceleration(self, reply_topic=None, **unused):
        data = self.read_acceleration()
        return self._publish_response("data/acceleration", {"source": self._name, "acceleration": data}, reply_topic)

    def _handle_read_magnetometer(self, reply_topic=None, **unused):
        data = self.read_magnetometer()
        return self._publish_response("data/magnetometer", {"source": self._name, "magnetometer": data}, reply_topic)

    def _handle_read_linear(self, reply_topic=None, **unused):
        data = self.read_linear_acceleration()
        return self._publish_response("data/linear", {"source": self._name, "linear_acceleration": data}, reply_topic)

    def _handle_read_gravity(self, reply_topic=None, **unused):
        data = self.read_gravity()
        return self._publish_response("data/gravity", {"source": self._name, "gravity": data}, reply_topic)

    def _handle_read_temperature(self, reply_topic=None, **unused):
        value = self.read_temperature()
        return self._publish_response("data/temperature", {"source": self._name, "temperature_c": value}, reply_topic)

    def _handle_get_status(self, reply_topic=None, **unused):
        status = self.get_system_status()
        payload = {"source": self._name, **status}
        return self._publish_response("data/status", payload, reply_topic)

    def _handle_get_calibration_status(self, reply_topic=None, **unused):
        status = self.get_calibration_status()
        return self._publish_response("data/calibration_status", {"source": self._name, "calibration": status}, reply_topic)

    def _handle_read_calibration(self, reply_topic=None, **unused):
        data = self.read_calibration_data()
        return self._publish_response("data/calibration", {"source": self._name, "calibration": data}, reply_topic)

    def _handle_set_operation_mode(self, mode, reply_topic=None, **unused):
        try:
            self.set_operation_mode(mode)
            payload = {"source": self._name, "operation_mode": self._operation_mode_name}
        except ValueError as exc:
            self._safe_log(f"Failed to set operation mode: {exc}", level="error")
            payload = {"source": self._name, "error": str(exc)}
        return self._publish_response("event/operation_mode", payload, reply_topic)

    def _handle_set_power_mode(self, mode, reply_topic=None, **unused):
        try:
            self.set_power_mode(mode)
            payload = {"source": self._name, "power_mode": self._power_mode_name}
        except ValueError as exc:
            self._safe_log(f"Failed to set power mode: {exc}", level="error")
            payload = {"source": self._name, "error": str(exc)}
        return self._publish_response("event/power_mode", payload, reply_topic)

    def _handle_save_calibration(self, filepath=None, reply_topic=None, **unused):
        target = filepath or self._calibration_file
        if not target:
            error = "Calibration file path required"
            self._safe_log(error, level="error")
            return self._publish_response("event/calibration_save", {"source": self._name, "error": error}, reply_topic)
        try:
            self.save_calibration_to_file(target)
            payload = {"source": self._name, "calibration_file": target, "status": "saved"}
            self._safe_log(f"Saved calibration data to {target}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self._safe_log(f"Failed to save calibration: {exc}", level="error")
            payload = {"source": self._name, "error": str(exc)}
        return self._publish_response("event/calibration_save", payload, reply_topic)

    def _handle_load_calibration(self, filepath=None, calibration=None, reply_topic=None, **unused):
        try:
            if calibration is not None:
                self.load_calibration_data(calibration)
                source = "payload"
            else:
                target = filepath or self._calibration_file
                if not target:
                    raise ValueError("Calibration file path required")
                self.load_calibration_from_file(target)
                source = target
            payload = {"source": self._name, "status": "loaded", "calibration_source": source}
            self._safe_log(f"Calibration data loaded from {source}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self._safe_log(f"Failed to load calibration: {exc}", level="error")
            payload = {"source": self._name, "error": str(exc)}
        return self._publish_response("event/calibration_load", payload, reply_topic)

    def _handle_debug_loop(self, *args, **kwargs):
        """Publish all readable sensor values whenever system loop ticks."""
        try:
            euler = self.read_euler()
            quaternion = self.read_quaternion()
            gyro = self.read_gyroscope()
            accel = self.read_acceleration()
            mag = self.read_magnetometer()
            linear = self.read_linear_acceleration()
            gravity = self.read_gravity()
            temperature = self.read_temperature()
            status = self.get_system_status()
            calib = self.get_calibration_status()
        except OSError as exc:
            self._safe_log(f"Debug poll failed: {exc}", level="warning")
            return

        reply_topic = kwargs.get('reply_topic')
        self._publish_response("data/euler", {"source": self._name, "euler": euler}, reply_topic)
        self._publish_response("data/quaternion", {"source": self._name, "quaternion": quaternion}, reply_topic)
        self._publish_response("data/gyroscope", {"source": self._name, "gyroscope": gyro}, reply_topic)
        self._publish_response("data/acceleration", {"source": self._name, "acceleration": accel}, reply_topic)
        self._publish_response("data/magnetometer", {"source": self._name, "magnetometer": mag}, reply_topic)
        self._publish_response("data/linear", {"source": self._name, "linear_acceleration": linear}, reply_topic)
        self._publish_response("data/gravity", {"source": self._name, "gravity": gravity}, reply_topic)
        self._publish_response("data/temperature", {"source": self._name, "temperature_c": temperature}, reply_topic)
        self._publish_response("data/status", {"source": self._name, **status}, reply_topic)
        self._publish_response("data/calibration_status", {"source": self._name, "calibration": calib}, reply_topic)

    def _read_vector(self, register, scale):
        raw = self._read_bytes(register, 6)
        return [self._twos_complement(raw[i] | (raw[i + 1] << 8)) / scale for i in range(0, 6, 2)]

    def _read_byte(self, register):
        return self.bus.read_byte_data(self.address, register)

    def _read_bytes(self, register, length):
        return self.bus.read_i2c_block_data(self.address, register, length)

    def _write_byte(self, register, value):
        self.bus.write_byte_data(self.address, register, value & 0xFF)

    def _write_bytes(self, register, data):
        chunk = list(data)
        self.bus.write_i2c_block_data(self.address, register, [byte & 0xFF for byte in chunk])

    def _safe_log(self, message, level="info"):
        try:
            self.log(message, level=level)
        except ValueError:
            pass

    def _safe_publish(self, topic, **payload):
        if not topic:
            return
        try:
            self.publish(topic, **payload)
        except ValueError:
            pass

    def _publish_response(self, default_suffix, payload, reply_topic=None):
        topic = reply_topic or self._topic(default_suffix)
        if topic:
            self._safe_publish(topic, **payload)
        return payload

    def _topic(self, suffix=None):
        base = f"bno055/{self._name}" if self._name else "bno055"
        if not suffix:
            return base
        return f"{base}/{suffix}"

    @staticmethod
    def _twos_complement(value):
        if value >= 0x8000:
            value -= 0x10000
        return value

    @staticmethod
    def _signed_byte(value):
        return value - 0x100 if value > 0x7F else value

    @staticmethod
    def _compute_unit_selection(units):
        value = 0x00
        if units.get("acceleration", "mps2").lower() in ("mps2", "m/s^2", "m/s2"):
            value |= 0x01
        if units.get("angular_rate", "dps").lower() in ("rad/s", "rps", "radians"):
            value |= 0x02
        if units.get("euler", "degrees").lower() in ("radians", "rad"):
            value |= 0x04
        if units.get("temperature", "c").lower() in ("f", "fahrenheit"):
            value |= 0x08
        return value

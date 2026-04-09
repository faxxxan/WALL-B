# WALL-B Troubleshooting Guide

This guide covers common issues and solutions for the WALL-B robot project. Each section addresses a specific component or symptom.

## Table of Contents

- [Servo Problems](#servo-problems)
- [Serial Communication Errors](#serial-communication-errors)
- [Arduino Mega Issues](#arduino-mega-issues)
- [Raspberry Pi Issues](#raspberry-pi-issues)
- [IMX500 Camera Problems](#imx500-camera-problems)
- [MPU6050 IMU Issues](#mpu6050-imu-issues)
- [ROS2 Node Failures](#ros2-node-failures)
- [Power and Battery Issues](#power-and-battery-issues)
- [Software Installation Problems](#software-installation-problems)

---

## Servo Problems

### Servo Not Responding

**Symptoms:**
- Servo doesn't move when commanded
- Servo jittering or twitching
- Servo stuck in one position

**Diagnosis Steps:**

1. **Check power supply:**
   ```bash
   # Measure voltage at servo bus with multimeter
   # Should read 6.0V - 7.4V
   # Low voltage = insufficient power
   ```

2. **Test servo directly:**
   ```bash
   # Disconnect servo from Arduino
   # Connect servo directly to 5V and GND
   # If servo still doesn't work, servo is faulty
   ```

3. **Check signal connection:**
   ```bash
   # Use oscilloscope or logic analyzer
   # Verify PWM signal at servo connector
   # Should be 50Hz with 1-2ms pulse width
   ```

**Solutions:**

| Cause | Solution |
| --- | --- |
| No power to servo | Check buck converter output, verify connections |
| Signal wire disconnected | Re-solder or replace signal wire |
| Servo failure | Replace servo motor |
| Software not sending commands | Verify serial communication |
| Wrong PWM pin | Check pin assignments in firmware |

**Code Test:**
```python
# Test servo with Python
import serial

# Send direct servo command
ser = serial.Serial('/dev/ttyUSB0', 115200)
# Command format: FF 01 servo_id position_low position_high checksum 0A
command = bytes([0xFF, 0x01, 0x00, 0xDC, 0x05, 0x00, 0x0A])
ser.write(command)
```

### Servo Jittering or Oscillating

**Symptoms:**
- Servo moves erratically
- Oscillation around target position
- Buzzing sound from servo

**Causes and Solutions:**

1. **Insufficient power:**
   - Increase voltage to 7.0-7.4V
   - Use higher capacity battery
   - Reduce number of servos moving simultaneously

2. **Mechanical binding:**
   - Check for obstructions in gear train
   - Verify bearings are properly lubricated
   - Check for debris in servo gears

3. **PID tuning needed:**
   - Adjust PID parameters in firmware
   - Increase derivative gain for damping
   - Reduce proportional gain if overshooting

4. **Signal interference:**
   - Route servo wires away from motor wires
   - Add ferrite cores to signal cables
   - Use shielded cable for long runs

### Servo Overheating

**Symptoms:**
- Servo too hot to touch (>60°C)
- Burning smell
- Servo becomes unresponsive after heating

**Solutions:**

1. **Reduce load:**
   - Check for mechanical binding
   - Reduce travel range
   - Use higher torque servos for legs

2. **Reduce current draw:**
   - Lower servo voltage to 6.0V
   - Implement smooth motion profiles
   - Don't stall servos at endpoints

3. **Improve cooling:**
   - Add heat sink to servo case
   - Improve airflow around servos
   - Reduce duty cycle of servo movement

---

## Serial Communication Errors

### Arduino Not Detected

**Symptoms:**
- `/dev/ttyUSB0` doesn't appear
- Permission denied errors
- "Device not found" messages

**Diagnosis:**

```bash
# List all serial devices
ls -la /dev/tty*

# Check USB devices
lsusb

# Check dmesg for USB events
dmesg | grep -i usb
dmesg | grep -i tty
```

**Solutions:**

| Issue | Solution |
| --- | --- |
| USB cable is power-only | Use data-capable USB cable |
| USB port malfunction | Try different USB port |
| Missing driver | Install CH340/FTDI driver |
| Permission denied | Add user to dialout group |

```bash
# Fix permission
sudo usermod -a -G dialout $USER
# Log out and back in

# Or temporarily use sudo
sudo chmod 666 /dev/ttyUSB0
```

### Communication Timeout

**Symptoms:**
- Commands sent but no response
- Partial responses received
- Intermittent communication failures

**Diagnosis:**

```bash
# Test with Arduino Serial Monitor
arduino-cli monitor --port /dev/ttyUSB0 --baudrate 115200

# Check forCTS/RTS handshake issues
stty -F /dev/ttyUSB0 -crtscts
```

**Solutions:**

1. **Check wiring:**
   - Verify TX/RX connections aren't crossed
   - Check for loose header pins
   - Verify ground connection

2. **Adjust serial settings:**
   ```python
   ser = serial.Serial(
       '/dev/ttyUSB0',
       baudrate=115200,
       timeout=1,  # Increase timeout
       xonxoff=False,
       rtscts=False
   )
   ```

3. **Add error handling:**
   ```python
   try:
       ser.write(command)
       response = ser.read(100)
   except serial.SerialException as e:
       print(f"Serial error: {e}")
       # Reconnect
       ser.close()
       time.sleep(1)
       ser.open()
   ```

### Corrupted Data / Framing Errors

**Symptoms:**
- Garbage characters in output
- Random servo movements
- Checksum failures

**Solutions:**

1. **Lower baud rate:**
   - Change to 57600 or 9600
   - Update both Arduino and Python code

2. **Add capacitors:**
   - Add 100µF capacitor across servo power
   - Add 0.1µF capacitors near Arduino

3. **Implement packet retry:**
   ```python
   def send_command(cmd, retries=3):
       for attempt in range(retries):
           ser.write(cmd)
           response = ser.read(100)
           if validate_checksum(response):
               return response
           time.sleep(0.1)
       raise CommunicationError("Failed after retries")
   ```

---

## Arduino Mega Issues

### Sketch Won't Upload

**Symptoms:**
- Upload fails with error
- "Device not found" during upload
- "Not in sync" error

**Solutions:**

1. **Check bootloader:**
   - Tools → Board → Arduino Mega 2560
   - Tools → Processor → ATmega2560
   - Tools → Port → Correct port

2. **Press reset before upload:**
   - Some boards need manual reset
   - Press reset button right before clicking upload

3. **Check memory:**
   ```bash
   # Use Arduino CLI to check sketch size
   arduino-cli compile --fqbn arduino:avr:mega --show-properties
   ```

4. **Reinstall bootloader (last resort):**
   - Use ISP programmer
   - Tools → Burn Bootloader

### Sketch Crashes / Reboots

**Symptoms:**
- Arduino resets randomly
- LED blinks rapidly (watchdog)
- Serial output cuts off

**Solutions:**

1. **Check memory usage:**
   ```cpp
   // Add to sketch to check memory
   Serial.print("Free RAM: ");
   Serial.println(freeMemory());
   ```

2. **Reduce array sizes:**
   - Decrease buffer sizes
   - Use PROGMEM for constant data

3. **Add watchdog:**
   ```cpp
   #include <avr/wdt.h>

   void setup() {
       wdt_enable(WDTO_2S);  // 2 second watchdog
   }

   void loop() {
       wdt_reset();
       // Your code
   }
   ```

### Analog Readings Unstable

**Symptoms:**
- Fluctuating sensor readings
- ADC values jumping randomly
- Noise in analog measurements

**Solutions:**

1. **Add filtering:**
   ```cpp
   int readAnalog(int pin, int samples = 10) {
       long sum = 0;
       for (int i = 0; i < samples; i++) {
           sum += analogRead(pin);
       }
       return sum / samples;
   }
   ```

2. **Add hardware filter:**
   - 100µF capacitor across AREF and GND
   - 0.1µF capacitor on each analog input

3. **Use external ADC:**
   - Add ADS1115 I2C ADC module
   - Provides 16-bit precision

---

## Raspberry Pi Issues

### SSH Connection Refused

**Symptoms:**
- "Connection refused" when SSHing
- "No route to host"
- Cannot find `wallb.local`

**Solutions:**

```bash
# Find Pi on network
nmap -sn 192.168.1.0/24 | grep -i raspberry

# Try direct IP
ssh pi@192.168.1.xx

# Check SSH service
sudo systemctl status ssh

# Enable SSH if needed
sudo systemctl enable ssh
sudo systemctl start ssh
```

### WiFi Not Connecting

**Solutions:**

```bash
# Scan for networks
sudo iwlist wlan0 scan | grep ESSID

# Edit WiFi config
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Add:
```conf
network={
    ssid="YourNetworkName"
    psk="YourPassword"
}
```

```bash
# Restart networking
sudo wpa_cli reconfigure
# Or
sudo systemctl restart networking
```

### Raspberry Pi Won't Boot

**Symptoms:**
- No HDMI output
- Power LED off or blinking
- Green LED shows pattern

**LED Patterns (Pi 4/5):**
| Pattern | Meaning |
| --- | --- |
| 1 flash | Bootloader not started |
| 3 flashes | Boot ROM not found |
| 4 flashes | SDRAM not found |
| 7 flashes | Kernel not found |

**Solutions:**

1. **Check power supply:**
   - Use official Raspberry Pi power supply
   - 5.1V 3A minimum for Pi 5

2. **Check SD card:**
   - Re-flash with fresh image
   - Check card is inserted properly

3. **Check HDMI:**
   - Try different HDMI cable
   - Try different monitor

---

## IMX500 Camera Problems

### Camera Not Detected

**Diagnosis:**

```bash
# Check camera is detected
vcgencmd get_camera

# Expected output:
# supported=1 detected=1

# List video devices
ls -la /dev/video*

# Check libcamera
libcamera-hello --list-cameras
```

**Solutions:**

1. **Enable camera interface:**
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   sudo reboot
   ```

2. **Check ribbon cable:**
   - Reseat CSI connector
   - Check for damage on cable
   - Ensure proper orientation (silver contacts toward HDMI)

3. **Update firmware:**
   ```bash
   sudo rpi-update
   sudo reboot
   ```

### No Image / Black Screen

**Diagnosis:**

```bash
# Test capture
libcamera-still -o test.jpg -t 5000

# Check for errors
dmesg | grep -i camera
```

**Solutions:**

1. **Focus adjustment:**
   - Rotate lens module
   - If using IR camera, focus may need adjustment

2. **Check light conditions:**
   - IR cameras need IR lighting
   - Try in well-lit environment

3. **Firmware issue:**
   ```bash
   # Reinstall camera stack
   sudo apt install --reinstall libcamera-apps
   ```

### AI Features Not Working

**Symptoms:**
- Object detection returns no results
- Face detection fails
- AI inference errors

**Solutions:**

1. **Install IMX500 firmware:**
   ```bash
   sudo apt install -y imx500-all
   ```

2. **Check model files:**
   ```bash
   ls /usr/share/imx500-models/
   # Should contain .aimet files
   ```

3. **Update IMX500 firmware:**
   ```bash
   # Download latest firmware from Sony
   rpi-update
   sudo reboot
   ```

---

## MPU6050 IMU Issues

### IMU Not Detected on I2C

**Diagnosis:**

```bash
# Scan I2C bus
sudo i2cdetect -y 1

# Expected: 0x68 or 0x69
```

**Solutions:**

| Address Missing | Solution |
| --- | --- |
| Pull-up resistors | Add 4.7KΩ resistors SDA/SCL to 3.3V |
| Wire broken | Check SDA/SCL connections |
| IMU damaged | Test with known-good IMU |
| I2C not enabled | Run `sudo raspi-config` → enable I2C |

### IMU Readings Stuck or Wrong

**Symptoms:**
- Accelerometer shows same value
- Gyroscope values don't change
- Values way off expected range

**Solutions:**

1. **Check wiring:**
   - Verify SDA → GPIO2 (Pin 3)
   - Verify SCL → GPIO3 (Pin 5)
   - Check 3.3V and GND

2. **Test with known-good code:**
   ```python
   from mpu6050 import mpu6050

   sensor = mpu6050(0x68)
   accel = sensor.get_accel_data()
   gyro = sensor.get_gyro_data()
   print(f"Accel: {accel}")
   print(f"Gyro: {gyro}")
   ```

3. **Calibrate IMU:**
   - Place IMU flat
   - Run calibration script
   - Record offset values
   - Apply offsets in code

### Noisy IMU Data

**Symptoms:**
- Jittery angle readings
- Robot drifts when stationary
- Large variance in measurements

**Solutions:**

1. **Implement complementary filter:**
   ```python
   alpha = 0.98
   angle = alpha * (angle + gyro_rate * dt) + (1 - alpha) * accel_angle
   ```

2. **Use Kalman filter:**
   - Install `filterpy` library
   - Implement 1D or 2D Kalman filter

3. **Hardware filtering:**
   - Add low-pass filter capacitor
   - Use higher quality IMU

---

## ROS2 Node Failures

### Node Won't Start

**Diagnosis:**

```bash
# List active nodes
ros2 node list

# Check node info
ros2 node info /wallb_servo_controller

# Check for errors
ros2 doctor
```

**Solutions:**

1. **Source ROS2 workspace:**
   ```bash
   source /opt/ros/humble/setup.bash
   source ~/wallb/ros2_ws/install/setup.bash
   ```

2. **Check dependencies:**
   ```bash
   rosdep install --from-paths src --ignore-src -y
   ```

3. **Rebuild workspace:**
   ```bash
   cd ~/wallb/ros2_ws
   colcon build --symlink-install
   ```

### Topic Not Publishing

**Diagnosis:**

```bash
# List topics
ros2 topic list

# Echo topic
ros2 topic echo /joint_states

# Check node permissions
ros2 run wallb_control servo_controller --ros-args -p debug:=true
```

**Solutions:**

1. **Check launch file:**
   - Verify node is included in launch file
   - Check for typos in node name

2. **Check remapping:**
   - Verify topic names match

3. **Add debug output:**
   ```python
   self.get_logger().info(f"Publishing: {data}")
   ```

### Inter-Process Communication Fails

**Symptoms:**
- Nodes can't communicate
- Messages not received
- High latency

**Solutions:**

1. **Check ROS_DOMAIN_ID:**
   ```bash
   # Both machines must have same domain
   export ROS_DOMAIN_ID=42
   echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
   ```

2. **Check network:**
   ```bash
   # Ping between machines
   ping <other_ip>

   # Check ROS discovery
   ros2 topic list --verbose
   ```

3. **Use namespaces:**
   - Add namespace to avoid conflicts
   - Update all references

---

## Power and Battery Issues

### Robot Cuts Out Under Load

**Symptoms:**
- Servos freeze when moving multiple joints
- Raspberry Pi reboots
- Arduino resets

**Solutions:**

1. **Check battery voltage:**
   - Measure under load with multimeter
   - Should stay above 10.5V for 3S LiPo
   - If dropping, battery is weak

2. **Use higher capacity battery:**
   - Upgrade from 2200mAh to 5000mAh
   - Use 4S LiPo for more headroom

3. **Limit simultaneous servo movement:**
   - Move servos sequentially
   - Reduce number of active servos

4. **Add capacitor bank:**
   - 2200µF capacitor near servo power input
   - Helps with transient loads

### Battery Drains Quickly

**Solutions:**

1. **Calculate current draw:**
   ```
   22 servos × 1A stall (worst case) = 22A
   But typical operating ~100mA per servo = 2.2A
   Add Pi (1A) + Arduino (0.1A) = ~3.3A operating
   ```

2. **Implement power saving:**
   - Reduce servo holding torque when idle
   - Turn off sensors not in use
   - Use sleep modes

3. **Use higher voltage battery:**
   - 4S (14.8V) reduces current for same power
   - Use buck converter to regulate

### Unexpected Shutdowns

**Solutions:**

1. **Add battery protection:**
   - Use LiPo battery with built-in protection
   - Add external protection circuit
   - Monitor battery voltage in software

2. **Implement low-voltage cutoff:**
   ```python
   if battery_voltage < 10.5:
       # Enter safe mode
       disable_all_servos()
       save_state()
       shutdown()
   ```

---

## Software Installation Problems

### pip Install Fails

**Solutions:**

```bash
# Update pip first
pip install --upgrade pip

# Use specific version
pip install numpy==1.24.0

# Use system package manager
sudo apt install python3-numpy

# Mirror or cache
pip install --index-url https://pypi.org/simple/ numpy
```

### ROS2 Install Fails

**Solutions:**

1. **Check Ubuntu version:**
   ```bash
   lsb_release -a
   # ROS2 Humble requires Ubuntu 22.04
   ```

2. **Clean install:**
   ```bash
   # Remove partial install
   sudo rm -rf /opt/ros/humble
   sudo rm -rf ~/ros2_ws

   # Follow installation guide exactly
   ```

3. **Use Docker (alternative):**
   ```bash
   # Use pre-built ROS2 Docker image
   docker run -it ros:humble
   ```

### Git Clone Fails

**Solutions:**

```bash
# Check network
ping github.com

# Use SSH instead of HTTPS
git clone git@github.com:faxxxan/WALL-B.git

# Or use token authentication
git clone https://github.com/faxxxan/WALL-B.git
# Use personal access token when prompted
```

### Import Errors in Python

**Symptoms:**
- `ModuleNotFoundError`
- `ImportError`

**Solutions:**

```bash
# Check Python path
python3 -c "import sys; print(sys.path)"

# Verify package installed
pip show <package-name>

# Reinstall in virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Check Python version
python3 --version  # Need 3.10+
```

---

## Getting More Help

If you've tried these solutions and still have issues:

1. **Check GitHub Issues:**
   - Search for similar issues
   - Check closed issues for solutions

2. **Collect diagnostic information:**
   ```bash
   # Create diagnostic report
   echo "=== System Info ===" > diagnostics.txt
   uname -a >> diagnostics.txt
   cat /etc/os-release >> diagnostics.txt
   echo "=== Python ===" >> diagnostics.txt
   python3 --version >> diagnostics.txt
   pip list >> diagnostics.txt
   echo "=== ROS2 ===" >> diagnostics.txt
   source /opt/ros/humble/setup.bash
   ros2 doctor >> diagnostics.txt
   ```

3. **Create new issue with:**
   - Clear title describing problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Diagnostic information
   - Photos/screenshots if relevant

---

## Contributing Solutions

If you solve an issue not covered here, consider contributing:

1. Fork the repository
2. Add your solution to this guide
3. Submit a pull request

Help others by sharing your experience!

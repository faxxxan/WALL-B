# WALL-B Software Setup Guide

This guide provides comprehensive instructions for setting up the WALL-B robot software, including all dependencies, configurations, and running the robot.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Raspberry Pi OS Setup](#raspberry-pi-os-setup)
- [Python Environment Setup](#python-environment-setup)
- [ROS2 Installation](#ros2-installation)
- [Arduino Firmware](#arduino-firmware)
- [WALL-B Software Installation](#wall-b-software-installation)
- [Configuration](#configuration)
- [Running the Robot](#running-the-robot)
- [Startup Scripts](#startup-scripts)

---

## Prerequisites

### Hardware Requirements

| Component | Requirement |
| --- | --- |
| Raspberry Pi | 5 (8GB recommended) or 4B |
| Storage | 32GB+ microSD card (Class A2) |
| Arduino | Mega 2560 |
| Power | 5V 3A USB-C for Pi, 11.1V+ LiPo for servos |
| Network | WiFi or Ethernet for initial setup |

### Software Requirements

| Software | Version | Purpose |
| --- | --- | --- |
| Raspberry Pi OS | 64-bit (Bookworm) | Operating System |
| Python | 3.10+ | Main programming language |
| ROS2 | Humble or Iron | Robotics middleware |
| Arduino CLI | Latest | Firmware compilation and upload |
| Git | Latest | Version control |

---

## Raspberry Pi OS Setup

### Step 1: Flash the OS

1. **Download Raspberry Pi Imager:**
   - Download from [raspberrypi.com/software](https://www.raspberrypi.com/software/)
   - Install on your computer

2. **Flash the image:**
   ```bash
   # Using Raspberry Pi Imager (GUI)
   # 1. Select "Raspberry Pi OS (64-bit)"
   # 2. Click the gear icon for advanced options:
   #    - Set hostname: wall-b
   #    - Enable SSH with password authentication
   #    - Set username/password: pi/wallb123
   #    - Configure WiFi (if needed)
   #    - Set locale settings
   # 3. Write to SD card
   ```

3. **Headless setup (optional):**
   - Create empty `ssh` file in boot partition
   - Create `userconf.txt` with encrypted password
   - Configure WiFi in `wpa_supplicant.conf`

### Step 2: Initial Boot

1. **Insert SD card and power on:**
   - Connect power to Raspberry Pi
   - Wait 2-3 minutes for first boot

2. **Connect via SSH:**
   ```bash
   ssh pi@wall-b.local
   # Password: wallb123
   ```

3. **Update system packages:**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo reboot
   ```

### Step 3: Enable Interfaces

1. **Open raspi-config:**
   ```bash
   sudo raspi-config
   ```

2. **Enable required interfaces:**
   - Interface Options → SSH → Enable
   - Interface Options → I2C → Enable
   - Interface Options → Camera → Enable (if using Pi camera)
   - Interface Options → Serial Port → Enable Serial UART
   - Performance Options → GPU Memory → 256MB (minimum)

3. **Reboot:**
   ```bash
   sudo reboot
   ```

---

## Python Environment Setup

### Step 1: Install Python and Dependencies

```bash
# Install Python and development tools
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y git cmake build-essential

# Install system dependencies for Python packages
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libgpiod2 python3-libgpiod
sudo apt install -y i2c-tools
```

### Step 2: Create Virtual Environment

```bash
# Create project directory
mkdir -p ~/wallb && cd ~/wallb

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Python Packages

```bash
# Core dependencies
pip install numpy pyserial smbus2

# Computer vision
pip install opencv-python opencv-contrib-python

# ROS2 Python packages
pip install rclpy geometry_msgs sensor_msgs std_msgs

# Neopixel control
pip install rpi-ws281x adafruit-circuitpython-neopixel

# IMU sensor
pip install mpu6050-raspberrypi

# Optional: AI and ML
pip install tensorflow tensorrt  # For IMX500 AI features

# Utility packages
pip install python-dotenv pyyaml
```

### Step 4: Verify Installation

```bash
# Test Python environment
python3 --version  # Should be 3.10+
pip list | head -20

# Test serial port access
ls -la /dev/serial0

# Test I2C
sudo i2cdetect -y 1
# Should show addresses 0x68 (MPU6050) if connected
```

---

## ROS2 Installation

### Option 1: Full ROS2 Installation (Recommended)

```bash
# Set locale
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS2 repository
sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install -y curl gnupg lsb-release

# Add GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update and install ROS2
sudo apt update
sudo apt install -y ros-humble-ros-base ros-humble-ros2-contrib ros-humble-ros2-ctrl

# Install additional tools
sudo apt install -y python3-colcon-common-extensions python3-argparse

# Install Gazebo (optional, for simulation)
sudo apt install -y ros-humble-gazebo-ros-pkgs
```

### Option 2: Minimal ROS2 Installation

```bash
# Install just ROS2 base
sudo apt update
sudo apt install -y ros-humble-ros-base python3-colcon-common-extensions

# Install essential packages
sudo apt install -y ros-humble-launch-xml ros-humble-launch-yaml
sudo apt install -y ros-humble-tf-transformations ros-humble-tf2-ros
sudo apt install -y ros-humble-robot-state-publisher ros-humble-joint-state-publisher
```

### ROS2 Workspace Setup

```bash
# Create workspace
mkdir -p ~/wallb/ros2_ws/src
cd ~/wallb/ros2_ws

# Copy or link WALL-B ROS2 packages
ln -s ~/wallb/WALL-B/ros2/wallb_* src/

# Install dependencies
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -y

# Build workspace
colcon build --symlink-install

# Source workspace
echo "source ~/wallb/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## Arduino Firmware

### Step 1: Install Arduino CLI

```bash
# Download Arduino CLI
cd ~/wallb
curl -fsSL https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linux_ARM64.tar.bz2 -o arduino-cli.tar.bz2

# Extract
tar xjf arduino-cli.tar.bz2
rm arduino-cli.tar.bz2

# Make executable
chmod +x arduino-cli

# Move to bin directory
sudo mv arduino-cli /usr/local/bin/arduino-cli

# Verify installation
arduino-cli version
```

### Step 2: Configure Arduino CLI

```bash
# Create configuration directory
mkdir -p ~/.arduino

# Initialize configuration
arduino-cli config init

# Add Arduino Mega board package
arduino-cli core update-index
arduino-cli core install arduino:avr@1.8.6

# List installed cores
arduino-cli core list
```

### Step 3: Connect Arduino and Upload Firmware

1. **Connect Arduino Mega to Raspberry Pi via USB**

2. **Find the port:**
   ```bash
   # List connected boards
   arduino-cli board list
   # Should show: Arduino Mega 2560 on /dev/ttyUSB0
   ```

3. **Create firmware sketch:**
   ```bash
   # Create sketch directory
   mkdir -p wallb_servo_control
   cd wallb_servo_control

   # Copy firmware from WALL-B repo
   cp ~/wallb/WALL-B/arduino/servo_control/* ./
   ```

4. **Modify servo pin configuration if needed:**
   - Edit `config.h` to match your wiring
   - Verify all pin assignments match the [Electronics Guide](/docs/electronics.md)

5. **Compile firmware:**
   ```bash
   arduino-cli compile --fqbn arduino:avr:mega
   ```

6. **Upload firmware:**
   ```bash
   arduino-cli upload --fqbn arduino:avr:mega --port /dev/ttyUSB0
   ```

### Step 4: Verify Firmware Upload

```bash
# Open serial monitor (115200 baud)
arduino-cli monitor --port /dev/ttyUSB0 --baudrate 115200

# You should see initialization messages
# Press reset button if needed
```

---

## WALL-B Software Installation

### Step 1: Clone Repository

```bash
# Navigate to project directory
cd ~/wallb

# Clone repository
git clone https://github.com/faxxxan/WALL-B.git

# Or update existing clone
cd WALL-B
git pull origin main
```

### Step 2: Install WALL-B Python Package

```bash
# Navigate to WALL-B directory
cd ~/wallb/WALL-B

# Install in development mode
pip install -e .

# Or install all required packages
pip install -r requirements.txt
```

### Step 3: Configure Robot Settings

1. **Copy configuration template:**
   ```bash
   cp configs/robot_config.yaml.example configs/robot_config.yaml
   ```

2. **Edit configuration:**
   ```yaml
   # Edit with your settings
   nano configs/robot_config.yaml
   ```

3. **Key configuration options:**
   ```yaml
   robot:
     name: "WALL-B"
     serial_port: "/dev/ttyUSB0"
     baud_rate: 115200

   servos:
     count: 22
     neutral_positions: [1500, 1500, ...]  # Microseconds

   sensors:
     imu:
       i2c_address: 0x68
       orientation: "forward"

   network:
     hostname: "wall-b"
     mqtt_broker: "192.168.1.100"  # Optional
   ```

### Step 4: Test Basic Connections

```bash
# Activate environment
source ~/wallb/venv/bin/activate

# Test serial connection
python3 -c "import serial; s = serial.Serial('/dev/ttyUSB0', 115200); print('Serial OK')"

# Test Arduino communication
python3 python/serial_test.py

# Test servo response
python3 python/servo_test.py --servo 0 --position 1500
```

---

## Configuration

### Serial Communication Setup

```bash
# Add user to dialout group (for serial access)
sudo usermod -a -G dialout $USER

# Log out and back in for group change to take effect
# Or use newgrp
newgrp dialout
```

### I2C Configuration

```bash
# Verify I2C is working
sudo i2cdetect -y 1

# Expected output:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:                         -- -- -- -- -- -- -- --
# 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 50: -- -- -- -- -- -- -- 58 -- -- -- -- -- -- -- --
# 60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
# 70: -- -- -- -- -- -- -- --
# (0x68 = MPU6050, 0x58 = RCWL-0516 or other sensor)
```

### Camera Configuration

```bash
# Test camera
libcamera-hello

# Capture test image
libcamera-still -o test.jpg

# If using IMX500 AI camera
# Install IMX500 firmware and libraries
sudo apt install -y imx500-all
```

### Network Configuration (Optional)

For remote control and monitoring:

```bash
# Set static IP (optional)
sudo nano /etc/dhcpcd.conf

# Add:
# interface eth0
# static ip_address=192.168.1.100/24
# static routers=192.168.1.1
# static domain_name_servers=192.168.1.1
```

---

## Running the Robot

### Quick Start

```bash
# Activate environment
source ~/wallb/venv/bin/activate
source ~/wallb/ros2_ws/install/setup.bash

# Launch full robot stack
ros2 launch wallb_control full_robot.launch.py
```

### Individual Module Testing

**Test Servo Control:**
```bash
# Run servo test
python3 python/servo_test.py --servo 0 --position 1500

# Run all servos to neutral
python3 python/servo_all_neutral.py

# Run servo sweep test
python3 python/servo_sweep.py --servo 0 --min 1000 --max 2000
```

**Test IMU:**
```bash
# Run IMU test
python3 python/sensors/imu_test.py

# Should display real-time accelerometer and gyroscope values
```

**Test Vision:**
```bash
# Run camera node
python3 python/vision/camera_node.py

# Run face tracking
python3 python/vision/face_tracker.py
```

### ROS2 Launch Files

| Launch File | Description |
| --- | --- |
| `full_robot.launch.py` | Complete robot system |
| `servo_control.launch.py` | Servo control only |
| `sensors.launch.py` | Sensor nodes only |
| `vision.launch.py` | Camera and vision |
| `minimal.launch.py` | Basic functionality |

### Running Specific Nodes

```bash
# Servo control node
ros2 run wallb_control servo_controller

# IMU node
ros2 run wallb_sensors imu_publisher

# Camera node
ros2 run wallb_vision camera_node

# Joint state publisher
ros2 run wallb_control joint_state_publisher
```

---

## Startup Scripts

### Systemd Service (Recommended)

Create a systemd service for automatic startup:

```bash
# Create service file
sudo nano /etc/systemd/system/wallb.service
```

```ini
[Unit]
Description=WALL-B Robot Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/wallb/WALL-B
ExecStart=/home/pi/wallb/venv/bin/python3 python/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable wallb.service
sudo systemctl start wallb.service

# Check status
sudo systemctl status wallb.service

# View logs
journalctl -u wallb.service -f
```

### Bashrc Aliases

Add convenient aliases to `~/.bashrc`:

```bash
# WALL-B aliases
alias wallb='cd ~/wallb/WALL-B && source ~/wallb/venv/bin/activate && source ~/wallb/ros2_ws/install/setup.bash'
alias wallb-launch='ros2 launch wallb_control full_robot.launch.py'
alias wallb-test='python3 ~/wallb/WALL-B/python/servo_test.py'
alias wallb-log='journalctl -u wallb.service -f'
```

### Launch at Boot (Alternative)

Add to `~/.config/autostart/wallb.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=WALL-B Robot
Exec=/home/pi/wallb/venv/bin/python3 /home/pi/wallb/WALL-B/python/main.py
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
```

---

## Troubleshooting

### Common Issues

**Serial port permission denied:**
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Log out and back in
```

**ROS2 domain conflict:**
```bash
# Set unique domain for each robot
export ROS_DOMAIN_ID=42
echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
```

**Camera not detected:**
```bash
# Check camera is enabled
sudo raspi-config  # Enable camera interface

# Check camera connection
vcgencmd get_camera

# Test with libcamera
libcamera-hello
```

For more troubleshooting help, see the [Troubleshooting Guide](/docs/troubleshooting.md).

---

## Next Steps

After installation and testing:

1. Review the [Contributing Guidelines](/CONTRIBUTING.md) if you plan to contribute
2. Explore the Python modules in `python/` directory
3. Check the ROS2 packages in `ros2/` directory
4. Experiment with the animation system in `python/animation/`
5. Try the ChatGPT integration in `python/chatgpt/`

---

## Support

For issues or questions:
- Check existing [GitHub Issues](https://github.com/faxxxan/WALL-B/issues)
- Create a new issue with detailed information
- Include logs, error messages, and your configuration

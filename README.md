Account X :

CA:

# WALL-B - Modular Biped Robot

An autonomous/remote-controlled robot inspired by WALL-E, built with Arduino and Raspberry Pi.

![WALL-B Robot - Full Assembly](https://raw.githubusercontent.com/faxxxan/WALL-B/main/images/full_project_front_pi5.jpg)

**Open-Source Modular Bipedal Robot Platform - Arduino + Raspberry Pi Powered**

*Inspired by WALL-E, built with passion*

[![Stars](https://img.shields.io/github/stars/faxxxan/WALL-B?style=flat-square)](https://github.com/faxxxan/WALL-B/stargazers)
[![Forks](https://img.shields.io/github/forks/faxxxan/WALL-B?style=flat-square)](https://github.com/faxxxan/WALL-B/network)
[![Issues](https://img.shields.io/github/issues/faxxxan/WALL-B?style=flat-square)](https://github.com/faxxxan/WALL-B/issues)
[![Last Commit](https://img.shields.io/github/last-commit/faxxxan/WALL-B?style=flat-square)](https://github.com/faxxxan/WALL-B/commits)
[![Repo Size](https://img.shields.io/github/repo-size/faxxxan/WALL-B?style=flat-square)](https://github.com/faxxxan/WALL-B)
[![License](https://img.shields.io/github/license/faxxxan/WALL-B?style=flat-square)](https://github.com/faxxxan/WALL-B/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/faxxxan/WALL-B/ci.yml?style=flat-square)](https://github.com/faxxxan/WALL-B/actions/workflows/ci.yml)

[Overview](#overview) • [Specifications](#specifications) • [Assembly](#assembly) • [Software](#software-modules) • [Getting Started](#getting-started) • [Documentation](#documentation)

---

## Overview

WALL-B (Working Autonomous Life-Like Biped) is an open-source modular bipedal robot platform built with Arduino Mega 2560 and Raspberry Pi 5. The robot features 22 degrees of freedom (DOF) for expressive movement and stable bipedal locomotion.

This project provides a flexible framework for robotics development using Python and C++ on the Raspberry Pi and Arduino platforms. WALL-B builds on lessons learned from previous robotics projects, offering improved stability, larger build size, and enhanced features.

### Key Features

| Feature | Description |
| --- | --- |
| **22 DOF Bipedal Design** | 22 servos for expressive movement including head, neck, arms, and legs |
| **Modular Architecture** | Custom PCBs for Raspberry Pi and Arduino, supporting rapid prototyping |
| **High-Torque Servos** | SG5010 and TowerPro MG92B servos for reliable leg and arm movement |
| **Sony IMX500 AI Camera** | Real-time face tracking and object detection capabilities |
| **Sensor Integration** | MPU6050 IMU for balancing, RCWL-0516 microwave sensor for motion detection |
| **Neopixel LED Eyes** | Adafruit Neopixel Jewel for expressive robot eye animations |
| **Power Management** | USB-C PD and 18650 battery support with XL4015 buck converters |
| **3D Printed Body** | STL files available for printing all mechanical components |
| **ROS2 Compatible** | Full ROS2 Humble/Iron integration for advanced robotics applications |

### Assembly Preview

| **Head Assembly** Sony IMX500 AI Camera integration with pan-tilt servo mount. Features real-time face tracking and object detection. |
| --- |
| ![Head Assembly](https://raw.githubusercontent.com/faxxxan/WALL-B/main/images/assembly_head.png) |

| **Body Assembly** Central torso housing Raspberry Pi 5, power distribution, and main controller board. |
| --- |
| ![Body Assembly](https://raw.githubusercontent.com/faxxxan/WALL-B/main/images/assembly_body.png) |

| **Leg Assembly** Multi-DOF leg mechanism with high-torque servos for stable bipedal walking. |
| --- |
| ![Leg Assembly](https://raw.githubusercontent.com/faxxxan/WALL-B/main/images/assembly_leg.png) |

### Full Assembly

| **Complete Assembly View** Full robot assembly showing all mechanical components and wiring layout. |
| --- |
| ![Full Assembly](https://raw.githubusercontent.com/faxxxan/WALL-B/main/images/assembly_full.png) |

| **Neck Mechanism** 2-DOF neck joint for head movement with cable management system. |
| --- |
| ![Neck Mechanism](https://raw.githubusercontent.com/faxxxan/WALL-B/main/images/assembly_neck.png) |

---

## Specifications

### Hardware Overview

| Component | Specification |
| --- | --- |
| **Main Controller** | Raspberry Pi 5 (8GB RAM) |
| **Motion Controller** | Arduino Mega 2560 |
| **Camera** | Sony IMX500 AI Camera |
| **Radio** | RTL-SDR USB Dongle |
| **Servos** | High-Torque Digital Servos |
| **Power** | LiPo Battery Pack (11.1V / 14.8V) |
| **Communication** | WiFi, Bluetooth, I2C, Serial |

### Servo Configuration

| Location | Type | Quantity | Function |
| --- | --- | --- | --- |
| Head | Pan-Tilt | 2 | Camera orientation |
| Neck | Servo | 2 | Head movement |
| Arms | Standard | 6 | Arm articulation |
| Legs | High-Torque | 12 | Bipedal locomotion |
| **Total** |  | **22 DOF** |  |

### Degrees of Freedom (DOF)

```
                    HEAD (2 DOF)
                    ├── Pan (Yaw)
                    └── Tilt (Pitch)
                         │
                    NECK (2 DOF)
                    ├── Rotate
                    └── Tilt
                         │
            ┌────────────┼────────────┐
            │                         │
       LEFT ARM (3 DOF)          RIGHT ARM (3 DOF)
       ├── Shoulder Pitch        ├── Shoulder Pitch
       ├── Shoulder Roll         ├── Shoulder Roll
       └── Elbow                  └── Elbow
                         │
                    TORSO (0 DOF)
                         │
            ┌────────────┼────────────┐
            │                         │
       LEFT LEG (6 DOF)          RIGHT LEG (6 DOF)
       ├── Hip Yaw                ├── Hip Yaw
       ├── Hip Roll               ├── Hip Roll
       ├── Hip Pitch              ├── Hip Pitch
       ├── Knee Pitch             ├── Knee Pitch
       ├── Ankle Pitch            ├── Ankle Pitch
       └── Ankle Roll             └── Ankle Roll
```

**Total: 22 DOF**

---

## Software Modules

The software architecture is built on a modular design pattern, allowing each component to be developed, tested, and deployed independently.

### Core Modules

| Module | Description | Technology |
| --- | --- | --- |
| **Animation** | Motion sequence playback and keyframe animation | Python |
| **ChatGPT** | Conversational AI integration with OpenAI API | Python |
| **Vision** | Computer vision and image processing with IMX500 | Python, OpenCV |
| **Tracking** | Real-time object and face tracking | Python, TensorFlow |
| **TTS** | Text-to-speech synthesis | Python |
| **Servos** | Low-level servo PWM control | C++, Arduino |
| **Neopixel** | RGB LED visual feedback | Python |
| **RTLSDR** | Software-defined radio processing | Python |
| **Braillespeak** | Text to Braille audio conversion | Python |
| **Motion Detection** | Microwave sensor integration | Python |
| **PiServo** | Raspberry Pi servo control | Python |
| **Translator** | Multi-language translation | Python |
| **Serial Connection** | RPi-Arduino communication | Python |
| **Viam** | VIAM API integration | Python |

### System Architecture

```
graph TB
    subgraph "High-Level Control"
        AI[ChatGPT AI]
        VIS[Vision System]
        TTS[Text-to-Speech]
    end

    subgraph "Main Controller - Raspberry Pi 5"
        ROS[ROS2 Core]
        PY[Python Runtime]
        CAM[IMX500 AI Camera]
        SDR[RTL-SDR Radio]
        NEO[Neopixel LEDs]
    end

    subgraph "Motion Controller - Arduino"
        MC[Motion Controller]
        IMU[IMU Sensor]
        PWM[PWM Generator]
        BUZ[Buzzer]
    end

    subgraph "Actuators"
        HS[Head Servos x2]
        NS[Neck Servos x2]
        AS[Arm Servos x6]
        LS[Leg Servos x12]
    end

    AI <--> ROS
    VIS <--> ROS
    TTS <--> ROS

    ROS <--> PY
    PY <--> CAM
    PY <--> SDR
    PY <--> NEO
    ROS <--> MC

    MC <--> IMU
    MC <--> PWM
    MC <--> BUZ

    PWM --> HS & NS & AS & LS
```

---

## Project Structure

```
WALL-B/
├── arduino/                    # Arduino firmware
│   ├── servo_control/          # Servo PWM control
│   ├── imu_fusion/             # IMU sensor fusion
│   └── communication/          # Serial communication
├── python/                     # Python modules
│   ├── animation/              # Motion sequences
│   ├── chatgpt/                # AI integration
│   ├── vision/                 # Computer vision
│   ├── tracking/               # Object tracking
│   ├── speech/                 # Voice interaction
│   ├── neopixel/               # LED control
│   ├── rtlsdr/                 # Radio processing
│   └── viam/                   # VIAM integration
├── ros2/                       # ROS2 packages
│   ├── wallb_control/          # Control package
│   ├── wallb_vision/           # Vision package
│   └── wallb_msgs/             # Custom messages
├── hardware/                   # Hardware designs
│   ├── cad/                    # 3D models (STL/STEP)
│   ├── pcb/                    # PCB schematics
│   └── bom/                    # Bill of materials
├── images/                     # Documentation images
├── docs/                       # Documentation
├── configs/                    # Configuration files
├── tests/                      # Test scripts
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Getting Started

### Prerequisites

| Requirement | Version |
| --- | --- |
| Python | 3.10+ |
| ROS2 | Humble / Iron |
| Arduino IDE | 2.0+ |
| CMake | 3.16+ |
| OpenCV | 4.5+ |

### Hardware Setup

1. **Raspberry Pi 5** - Flash Raspberry Pi OS (64-bit)
2. **Arduino Mega** - Connect via USB to Raspberry Pi
3. **IMX500 Camera** - Connect to CSI port
4. **Servos** - Wire to Arduino PWM pins
5. **Power** - Connect LiPo battery to power distribution board

### Software Installation

```bash
# Clone repository
git clone https://github.com/faxxxan/WALL-B.git
cd WALL-B

# Install Python dependencies
pip install -r requirements.txt

# Install ROS2 dependencies
rosdep install --from-paths ros2 --ignore-src -y

# Build ROS2 workspace
colcon build
source install/setup.bash

# Upload Arduino firmware
cd arduino/servo_control
arduino-cli compile --fqbn arduino:avr:mega
arduino-cli upload --fqbn arduino:avr:mega --port /dev/ttyUSB0
```

### Quick Start

```bash
# Launch full robot stack
ros2 launch wallb_control full_robot.launch.py

# Run standalone vision module
python python/vision/camera_node.py

# Test servo control
python python/servo_test.py --port /dev/ttyUSB0

# Start ChatGPT interaction
python python/chatgpt/chat_interface.py
```

---

## Roadmap

- [x] Core servo control firmware
- [x] Basic locomotion algorithms
- [x] IMX500 camera integration
- [x] ChatGPT API integration
- [x] Neopixel LED feedback
- [x] RTL-SDR radio module
- [ ] Advanced bipedal walking gait
- [ ] Real-time SLAM navigation
- [ ] Gesture recognition
- [ ] Voice wake word detection
- [ ] Mobile app control interface
- [ ] Cloud telemetry dashboard

---

## Documentation

| Category | Description |
| --- | --- |
| [Assembly Guide](docs/assembly.md) | Step-by-step assembly instructions |
| [Electronics Setup](docs/electronics.md) | Wiring diagrams and connections |
| [Software Setup](docs/software.md) | Software installation guide |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and solutions |

---

## Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Open Source Robotics Community** - ROS2 and related tools
- **Raspberry Pi Foundation** - Hardware platform
- **Arduino** - Microcontroller platform

---

**WALL-B Robotics**
*Building the Future of Personal Robotics - One Module at a Time*

---

<!--
================================================================================
REPOSITORY TOPICS
================================================================================
To improve discoverability, please add these topics to your repository via GitHub:
1. Go to https://github.com/faxxxan/WALL-B/settings
2. Click on "Topics" in the left sidebar
3. Add the following topics:

robot
robotics
raspberry-pi
arduino
biped-robot
open-source
python
ros2
servo
humanoid-robot
3d-printing
computer-vision
================================================================================
-->

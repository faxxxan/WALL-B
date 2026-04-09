# WALL-B Electronics Setup Guide

This guide provides detailed wiring diagrams, pin assignments, and electronic connections for the WALL-B robot.

## Table of Contents

- [Power Distribution](#power-distribution)
- [Arduino Mega Pin Assignments](#arduino-mega-pin-assignments)
- [Raspberry Pi GPIO Connections](#raspberry-pi-gpio-connections)
- [Sensor Wiring](#sensor-wiring)
- [Communication Protocols](#communication-protocols)
- [Wiring Diagrams](#wiring-diagrams)

---

## Power Distribution

### Power System Overview

The WALL-B robot uses a multi-voltage power distribution system to supply different components with appropriate voltages.

```
                    ┌─────────────────┐
                    │   LiPo Battery  │
                    │   11.1V / 14.8V  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Power Switch  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────────┐     │     ┌────────▼────────┐
     │  XL4015 Buck #1 │     │     │  XL4015 Buck #2 │
     │    Output: 7.4V │     │     │   Output: 5V    │
     └────────┬────────┘     │     └────────┬────────┘
              │              │              │
    ┌─────────┴─────────┐     │     ┌───────┴───────┐
    │   Servo Bus      │     │     │  Logic Power  │
    │   (All Servos)   │     │     │  (5V Rail)    │
    └──────────────────┘     │     └───────┬───────┘
                             │             │
                    ┌────────▼─────────────▼────────┐
                    │     Power Distribution PCB     │
                    └───────────────────────────────┘
```

### Voltage Rails

| Rail | Voltage | Current | Components |
| --- | --- | --- | --- |
| VBAT | 11.1V-14.8V | 10A+ | Battery direct |
| VSERVO | 6.0V-7.4V | 8A | All servos |
| V5V | 5.0V | 3A | Raspberry Pi, Arduino, Sensors |
| V3V3 | 3.3V | 500mA | Sensors, logic level conversion |

### Power Distribution Board

The main power distribution board (hardware/pcb/power_dist/) routes power to all components:

| Pin/Connector | Voltage | Function |
| --- | --- | --- |
| BAT_IN | 11.1-14.8V | Battery input (XT60 connector) |
| SW_OUT | 11.1-14.8V | Switched power output |
| SERVO_PWR | 6.0-7.4V | Servo bus (2-pin JST) |
| VCC_5V | 5.0V | Logic power (2-pin JST) |
| VCC_3V3 | 3.3V | Sensor power (2-pin JST) |
| GND | Ground | Common ground bus |

### Buck Converter Configuration

The XL4015 buck converters should be configured as follows:

**For Servo Power (7.4V):**
- Input: 11.1V-14.8V from battery
- Output: 7.4V (adjustable via potentiometer)
- Current limit: 5A per converter
- Use 2 converters in parallel for 12 leg servos

**For Logic Power (5V):**
- Input: 11.1V-14.8V from battery
- Output: 5.0V (fixed or adjustable)
- Current limit: 3A
- Powers Raspberry Pi, Arduino, sensors

### Battery Recommendations

| Battery Type | Voltage | Capacity | Weight | Notes |
| --- | --- | --- | --- | --- |
| 3S LiPo | 11.1V | 2200-5000mAh | 150-350g | Recommended |
| 4S LiPo | 14.8V | 2200-4000mAh | 200-400g | Higher voltage |
| 18650 Pack | 11.1V | 6000mAh | ~300g | Safer option |

---

## Arduino Mega Pin Assignments

The Arduino Mega 2560 controls all 22 servos using PWM signals. Each servo requires a dedicated PWM pin.

### Servo Pin Mapping

#### Head Servos (2 DOF)

| Servo | Arduino Pin | PWM Timer | Function |
| --- | --- | --- | --- |
| Head Pan | Pin 2 | Timer3 Channel 3 | Horizontal rotation |
| Head Tilt | Pin 3 | Timer3 Channel 2 | Vertical rotation |

#### Neck Servos (2 DOF)

| Servo | Arduino Pin | PWM Timer | Function |
| --- | --- | --- | --- |
| Neck Rotate | Pin 4 | Timer3 Channel 1 | Neck yaw |
| Neck Tilt | Pin 5 | Timer3 Channel 4 | Neck pitch |

#### Left Arm Servos (3 DOF)

| Servo | Arduino Pin | PWM Timer | Function |
| --- | --- | --- | --- |
| L Shoulder Pitch | Pin 6 | Timer4 Channel 1 | Shoulder up/down |
| L Shoulder Roll | Pin 7 | Timer4 Channel 2 | Shoulder rotation |
| L Elbow | Pin 8 | Timer4 Channel 3 | Elbow bend |

#### Right Arm Servos (3 DOF)

| Servo | Arduino Pin | PWM Timer | Function |
| --- | --- | --- | --- |
| R Shoulder Pitch | Pin 9 | Timer4 Channel 4 | Shoulder up/down |
| R Shoulder Roll | Pin 10 | Timer4 Channel 3 | Shoulder rotation |
| R Elbow | Pin 11 | Timer4 Channel 2 | Elbow bend |

#### Left Leg Servos (6 DOF)

| Servo | Arduino Pin | PWM Timer | Function |
| --- | --- | --- | --- |
| L Hip Yaw | Pin 12 | Timer4 Channel 1 | Hip rotation |
| L Hip Roll | Pin 13 | Timer4 Channel 2 | Hip side rotation |
| L Hip Pitch | Pin 44 | Timer5 Channel 3 | Hip forward/back |
| L Knee | Pin 45 | Timer5 Channel 2 | Knee bend |
| L Ankle | Pin 46 | Timer5 Channel 1 | Ankle pitch |
| L Ankle Roll | Pin 47 | Timer5 Channel 3 | Ankle roll |

#### Right Leg Servos (6 DOF)

| Servo | Arduino Pin | PWM Timer | Function |
| --- | --- | --- | --- |
| R Hip Yaw | Pin 48 | Timer5 Channel 3 | Hip rotation |
| R Hip Roll | Pin 49 | Timer5 Channel 1 | Hip side rotation |
| R Hip Pitch | Pin 50 | Timer5 Channel 2 | Hip forward/back |
| R Knee | Pin 51 | Timer5 Channel 3 | Knee bend |
| R Ankle | Pin 52 | Timer5 Channel 1 | Ankle pitch |
| R Ankle Roll | Pin 53 | Timer5 Channel 2 | Ankle roll |

### Complete Pin Map

```
Pin 0:  RX (Serial Communication with Raspberry Pi)
Pin 1:  TX (Serial Communication with Raspberry Pi)
Pin 2:  Head Pan Servo
Pin 3:  Head Tilt Servo
Pin 4:  Neck Rotate Servo
Pin 5:  Neck Tilt Servo
Pin 6:  Left Shoulder Pitch Servo
Pin 7:  Left Shoulder Roll Servo
Pin 8:  Left Elbow Servo
Pin 9:  Right Shoulder Pitch Servo
Pin 10: Right Shoulder Roll Servo
Pin 11: Right Elbow Servo
Pin 12: Left Hip Yaw Servo
Pin 13: Left Hip Roll Servo
Pin 44: Left Hip Pitch Servo
Pin 45: Left Knee Servo
Pin 46: Left Ankle Servo
Pin 47: Left Ankle Roll Servo
Pin 48: Right Hip Yaw Servo
Pin 49: Right Hip Roll Servo
Pin 50: Right Hip Pitch Servo
Pin 51: Right Knee Servo
Pin 52: Right Ankle Servo
Pin 53: Right Ankle Roll Servo
```

### I2C Pins

| Pin | Function | Connection |
| --- | --- | --- |
| Pin 20 (SDA) | I2C Data | MPU6050, external sensors |
| Pin 21 (SCL) | I2C Clock | MPU6050, external sensors |

### Analog Pins

| Pin | Function | Connection |
| --- | --- | --- |
| A0 | Battery Voltage Monitor | Via voltage divider |
| A1 | Current Sensor | Servo bus current sense |
| A2-A5 | Reserved | Expansion headers |

### Digital Pins

| Pin | Function | Connection |
| --- | --- | --- |
| Pin 22-23 | Neopixel Data | Adafruit Neopixel Jewel |
| Pin 24 | Buzzer | Active buzzer |
| Pin 25 | Status LED | Board status indicator |

### Serial Communication

| Connection | Pins | Protocol | Baud Rate |
| --- | --- | --- | --- |
| Raspberry Pi | 0 (RX), 1 (TX) | UART Serial | 115200 |

---

## Raspberry Pi GPIO Connections

### GPIO Pinout

```
    3.3V  ───────────────  5V
    GPIO2  ───────────────  5V
    GPIO3  ───────────────  GND
    GPIO4  ───────────────  GPIO14 (UART TX)
    GND  ───────────────  GPIO15 (UART RX)
    GPIO17  ───────────────  GPIO18
    GPIO27  ───────────────  GND
    GPIO22  ───────────────  GPIO23
    3.3V  ───────────────  GPIO24
    GPIO10  ───────────────  GND
    GPIO9  ───────────────  GPIO25
    GPIO11  ───────────────  GPIO8
    GND  ───────────────  GPIO7
    GPIO0  ───────────────  GPIO1
    GPIO5  ───────────────  GND
    GPIO6  ───────────────  GPIO12
    GPIO13  ───────────────  GND
    GPIO19  ───────────────  GPIO16
    GPIO26  ───────────────  GPIO20
    GND  ───────────────  GPIO21
```

### GPIO Usage in WALL-B

| GPIO | Function | Connection | Notes |
| --- | --- | --- | --- |
| GPIO0 | I2C SDA | MPU6050 SDA | 3.3V logic |
| GPIO1 | I2C SCL | MPU6050 SCL | 3.3V logic |
| GPIO2 | I2C SDA | External I2C sensors | 3.3V logic |
| GPIO3 | I2C SCL | External I2C sensors | 3.3V logic |
| GPIO14 | UART TX | Arduino Mega RX (Pin 0) | 3.3V to 5V logic level |
| GPIO15 | UART RX | Arduino Mega TX (Pin 1) | 3.3V to 5V logic level |
| GPIO18 | PWM (GPIO) | Neopixel Data | Via level shifter |
| GPIO23 | Status LED | Green LED | Activity indicator |
| GPIO24 | Status LED | Red LED | Error indicator |
| GPIO25 | Power Enable | Power distribution control | Active high |

### Logic Level Conversion

The Raspberry Pi GPIO operates at 3.3V, while the Arduino Mega uses 5V logic. Use bi-directional logic level converters:

**For UART Communication (RX/TX):**
- Module: BSS138 based 4-channel logic level shifter
- Connection: 3.3V side to Pi, 5V side to Arduino

**For I2C Sensors:**
- The MPU6050 and most sensors support 3.3V directly
- Use 4.7KΩ pull-up resistors to 3.3V if needed

### Raspberry Pi to Arduino Connection

```
Raspberry Pi          Logic Level          Arduino Mega
   GPIO14 (TX)  ───>  Converter  ───>  Pin 0 (RX)
   GPIO15 (RX)  <───  Converter  <───  Pin 1 (TX)
   GND          ────  Converter  ────  GND
```

---

## Sensor Wiring

### MPU6050 IMU Sensor

The MPU6050 provides 6-axis motion sensing (3-axis gyroscope + 3-axis accelerometer) for balance control.

**Specifications:**
- Voltage: 3.3V
- Interface: I2C
- I2C Address: 0x68 (or 0x69 with AD0 pin high)
- Axes: X, Y, Z for both gyro and accelerometer

**Wiring:**

| MPU6050 Pin | Raspberry Pi | Arduino Mega | Notes |
| --- | --- | --- | --- |
| VCC | 3.3V | 3.3V | Power supply |
| GND | GND | GND | Ground |
| SDA | GPIO2 (SDA) | Pin 20 (SDA) | I2C Data |
| SCL | GPIO3 (SCL) | Pin 21 (SCL) | I2C Clock |
| AD0 | GND | GND | Address 0x68 |

**Mounting Position:**
- Mount MPU6050 flat in the torso center
- Align X-axis with robot's forward direction
- Y-axis pointing left
- Z-axis pointing up

### RCWL-0516 Microwave Sensor

The RCWL-0516 is a microwave radar sensor used for motion detection and proximity sensing.

**Specifications:**
- Voltage: 4-28V (5V recommended)
- Output: Digital HIGH/LOW
- Detection Range: 5-7 meters
- Detection Angle: 360°

**Wiring:**

| RCWL-0516 Pin | Connection | Notes |
| --- | --- | --- |
| VIN | 5V | Power supply |
| GND | GND | Ground |
| OUT | GPIO27 (Pi) / Pin 26 (Mega) | Motion detected output |
| 3V3 | Not connected | Can power external 3.3V devices |

**Installation:**
- Mount on back of robot to detect approaching people
- Avoid metal surfaces near the sensor
- Keep antenna area clear

### IMX500 AI Camera

The Sony IMX500 AI camera provides edge AI capabilities including object detection and face tracking.

**Connection:**
- Connect to Raspberry Pi CSI port
- Use 15-pin ribbon cable (included with camera)

**Specifications:**
- Resolution: 12.3 MP
- Interface: MIPI CSI-2
- AI Capabilities: On-device object detection, people counting
- Output: Standard camera interface via libcamera

**Wiring Diagram:**

```
IMX500 Camera          Raspberry Pi 5
    CSI Connector  ──────  CSI Port
         │                      │
         │              Ribbon Cable
         │                      │
         ▼                      ▼
   Data (CSI-2)  ←────────  CSI Interface
```

### Buzzer

A passive buzzer provides audio feedback.

**Specifications:**
- Type: Passive buzzer (for tones)
- Voltage: 3.3V-5V
- Current: <30mA

**Wiring:**

| Buzzer Pin | Arduino Mega | Notes |
| --- | --- | --- |
| VCC/Positive | 5V (via resistor) | With 100Ω resistor |
| Signal | Pin 24 | PWM signal for tones |
| GND | GND | Ground |

### Neopixel LED Ring (Eye)

The Adafruit Neopixel Jewel provides expressive eye lighting.

**Specifications:**
- Voltage: 5V
- LEDs: 7 x WS2812B RGB LEDs
- Interface: Single wire protocol

**Wiring:**

| Neopixel Pin | Arduino Mega | Notes |
| --- | --- | --- |
| VCC | 5V | Power |
| GND | GND | Ground |
| Data In (DI) | Pin 22 | Data signal |
| Data Out (DO) | Optional | For chaining |

**Alternative (from Raspberry Pi):**
- Connect to GPIO18 via 3.3V to 5V logic level converter
- Use Raspberry Pi's neopixel library

---

## Communication Protocols

### Serial Communication (RPi ↔ Arduino)

The primary communication between Raspberry Pi and Arduino Mega uses UART serial.

**Protocol:**
- Baud Rate: 115200
- Data Bits: 8
- Stop Bits: 1
- Parity: None
- Flow Control: None

**Message Format:**
```
<START_BYTE> <CMD> <DATA...> <CHECKSUM> <END_BYTE>
```

| Field | Value | Description |
| --- | --- | --- |
| START_BYTE | 0xFF | Message start indicator |
| CMD | 0x00-0xFF | Command type |
| DATA | Variable | Command data payload |
| CHECKSUM | 0x00-0xFF | XOR checksum of CMD+DATA |
| END_BYTE | 0x0A | Message end indicator (newline) |

**Available Commands:**

| CMD | Name | Data | Description |
| --- | --- | --- | --- |
| 0x01 | SERVO_POS | servo_id, position (2 bytes) | Set servo position |
| 0x02 | SERVO_SPEED | servo_id, speed (2 bytes) | Set servo speed |
| 0x03 | SERVO_DISABLE | servo_id | Disable servo torque |
| 0x04 | SERVO_ENABLE | servo_id | Enable servo torque |
| 0x05 | GET_STATUS | - | Get Arduino status |
| 0x06 | SET_ALL | 22x position (44 bytes) | Set all servo positions |
| 0x07 | RESET | - | Reset Arduino |

### I2C Communication

I2C is used for connecting additional sensors and expansion boards.

**Configuration:**
- Bus: /dev/i2c-1 (Raspberry Pi)
- Speed: 400kHz (Fast Mode)
- Pull-ups: 4.7KΩ to 3.3V

**I2C Devices:**

| Device | Address | Notes |
| --- | --- | --- |
| MPU6050 | 0x68 | IMU sensor |
| ADS1115 | 0x48 | ADC expansion (optional) |
| PCA9685 | 0x40 | Servo expansion (optional) |

### SPI Communication

SPI is available for high-speed sensors and displays.

**Configuration:**
- Bus: /dev/spidev0.0
- Speed: 1MHz
- Mode: 0 (CPOL=0, CPHA=0)

---

## Wiring Diagrams

### Complete System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                           WALL-B Wiring                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                              ┌─────────────┐  │
│   │  LiPo Batt  │                              │  IMX500     │  │
│   │  11.1-14.8V │                              │  Camera     │  │
│   └──────┬──────┘                              └──────┬──────┘  │
│          │                                            │          │
│          ▼                                            ▼          │
│   ┌─────────────┐                              ┌─────────────┐  │
│   │Power Switch │                              │ Raspberry   │  │
│   └──────┬──────┘                              │    Pi 5     │  │
│          │                                       └──────┬──────┘  │
│          ├────────────────┐                            │          │
│          │                │                     ┌──────┴──────┐  │
│          ▼                ▼                     │ Serial 115200│  │
│   ┌─────────────┐   ┌─────────────┐             │    UART     │  │
│   │XL4015 #1    │   │XL4015 #2    │             └──────┬──────┘  │
│   │7.4V Servos  │   │5V Logic     │                    │          │
│   └──────┬──────┘   └──────┬──────┘                    │          │
│          │                │                            │          │
│          ▼                ▼                            │          │
│   ┌─────────────┐   ┌─────────────┐                    │          │
│   │Servo Bus    │   │ 5V Rail      │                    │          │
│   │(22 Servos)  │   │             │                    │          │
│   └──────┬──────┘   └──────┬──────┘                    │          │
│          │                │                            │          │
│          │         ┌──────┴──────┐                      │          │
│          │         │             │                      │          │
│          │         ▼             ▼                      │          │
│          │  ┌─────────────┐ ┌─────────────┐            │          │
│          │  │Arduino Mega  │ │  Sensors    │◄────────────┘          │
│          │  │  2560        │ │  MPU6050    │                       │
│          │  └─────────────┘ └─────────────┘                       │
│          │                                                         │
└──────────┼─────────────────────────────────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────────────────┐
    │              22 Servo Motors                 │
    │  Head(2) Neck(2) L.Arm(3) R.Arm(3)          │
    │  L.Leg(6) R.Leg(6)                          │
    └─────────────────────────────────────────────┘
```

### Detailed Servo Wiring (One Leg Example)

```
Arduino Mega                  Servo Connector Board
    │                               │
    │ Pin 44 ──────────────────────►│ Servo 1 (L Hip Pitch)
    │ Pin 45 ──────────────────────►│ Servo 2 (L Knee)
    │ Pin 46 ──────────────────────►│ Servo 3 (L Ankle)
    │ Pin 47 ──────────────────────►│ Servo 4 (L Ankle Roll)
    │ Pin 48 ──────────────────────►│ Servo 5 (L Hip Yaw)
    │ Pin 49 ──────────────────────►│ Servo 6 (L Hip Roll)
    │                               │
    │ Pin 51 ──────────────────────►│ Servo 7 (R Knee)
    │ Pin 52 ──────────────────────►│ Servo 8 (R Ankle)
    │ Pin 53 ──────────────────────►│ Servo 9 (R Ankle Roll)
    │                               │
    │        Servo Power Bus         │
    │ Pin 2-5V ◄────────────────────│ VSERVO (7.4V)
    │ Pin GND ◄─────────────────────│ Ground
    │                               │
    └───────────────────────────────┘
```

---

## Safety Guidelines

### Electrical Safety

1. **Always disconnect battery before wiring modifications**
2. **Use appropriate wire gauges for current requirements**
3. **Add fuses to power distribution:**
   - 10A fuse on main battery lead
   - 5A fuses on each buck converter output
4. **Verify polarity before connecting components**

### ESD Protection

1. **Use anti-static mats during assembly**
2. **Handle Arduino and Raspberry Pi with care**
3. **Avoid static discharge near electronics**

### Power-On Sequence

1. Verify all connections are secure
2. Check for short circuits with multimeter
3. Connect battery
4. Turn on power switch
5. Observe for smoke, heat, or unusual sounds
6. If abnormal, immediately disconnect power

### Power-Off Sequence

1. Shut down Raspberry Pi properly
2. Turn off power switch
3. Disconnect battery
4. Wait 30 seconds before any wiring changes

---

## Next Steps

After wiring is complete, proceed to the [Software Setup Guide](software.md) to install and configure the required software.

For troubleshooting electrical issues, see the [Troubleshooting Guide](troubleshooting.md).

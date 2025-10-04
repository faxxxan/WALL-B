# BaseModule Documentation

## Overview

Serial bus servos allow for efficient communication and control of multiple servos over a single bus. The `Servo` class provides an interface to manage these servos, including setting positions, speeds, and handling configurations.

## Configuration

The `config/servo_waveshare.yml` file contains the configuration for each bus servo. The `instances` section defines the servos, their IDs, and their initial positions. The `poses` section within each instance defines various poses that can be used to set servo positions.

## Getting Started

To calibrate the servos, each must have their ID set individually. To achieve this, connect one servo to the driver board and run `modules/actuators/bus_servo/change_id.py`. This script will prompt you to enter the ID for the connected servo, which will then be saved permanently on the servo.

If you have challenges understanding the current ID of the servo, run `modules/actuators/bus_servo/STServo_examples/read_all.py` or `modules/actuators/bus_servo/SCServo_examples/read_all.py` depending on the servo type. This script will read and display the current ID of the connected servo.

Note: if there is an issue with dependencies, you may need to run the script from within the `modules/actuators/bus_servo` directory.

Once this has been done for all servos, you can use the `Servo` class to control them by enabling it in the above yaml file.

To calibrate the servo positions, set the flag `calibrate_on_boot` to `true` in the configuration file for each instance (servo). This will cause the servo to output it's current position in the debug log, which can then be copied into the start position, or range. Servos can be manually moved to any position to identify their range or certain poses.

Note: calibrate_on_boot is enabled by default to help with initial configuration.

Once the start position and range are set, move the flag to the next servo and repeat the process until all servos are calibrated.

Finally, set `calibrate_on_boot` to false and re-run the program to start using the servos with their configured positions.

## Subscriptions

The `Servo` class subscribes to the following topics:
`servo:<identifier>:mv` - to move the servo to a specific position relative to it's current position.
`servo:<identifier>:mvabs` - to move the servo to a specific position with absolute values.

## Smooth initialization

Because the `Servo` class gets the current position of the servo on initialization, there is no danger of a servo jumping from an unknown position to the start position. This is especially useful when the servos are powered on in a random position and is an advantage over hobby servos used in previous versions of the modular biped.

## SC vs ST servos

The `Servo` class supports both ST and SC series servos from Waveshare. The type of servo is determined by the `model` variable in the configuration file. The class will automatically use the appropriate SDK for the specified servo type.

There are some limitations to the SC servos as they do not support continuous rotation and have a lower rotational range compared to the ST servos. 

## References
https://www.waveshare.com/wiki/ST3215_Servo
https://www.waveshare.com/wiki/SC09_Servo
https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A)
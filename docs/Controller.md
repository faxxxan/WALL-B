# Controller Module Documentation

## Overview

The `Controller` module provides an interface for using a game controller (such as an Xbox or PlayStation controller) to control the robot via Bluetooth or USB. It allows mapping of controller buttons and analog axes to publish events on the robot's messaging system, enabling real-time teleoperation and custom control schemes.

## Enable controller on ubuntu:

<!-- sudo apt install dkms linux-headers-$(uname -r)
git clone https://github.com/atar-axis/xpadneo.git
cd xpadneo
sudo ./install.sh -->
<!-- Did not work -->

## Configuration

The `config/controller.yml` file contains the configuration for the controller module. The `button_action_map` section supports dynamic remapping based on any pressed modifier button or combination. 

The `deadzone` parameter can be set globally or per-axis to filter out small analog stick movements. The `modifier_buttons` list defines which buttons act as modifiers for remapping.

### Example Configuration
```yaml
controller:
  enabled: true
  path: modules.controller.Controller
  config:
    deadzone: 500  # Global deadzone for analog axes
    button_action_map:
      default:
        BTN_A: # Upon pressing 'A' button on controller, speak message
          - topic: 'tts'
            args: {msg: 'Test Default'}
        ABS_X: # Use x axis of left thumbstick to control eye position
          - topic: 'eye/look'
            args: {axis: 'x'}
            modifier:
              scale: 1.0
      BTN_BL: # When left shoulder button is pressed
        BTN_A: # 'A' button speaks different messages
          - topic: 'tts'
            args: {msg: 'Left Shoulder Pressed'}
        ABS_X: # Use x axis of left thumbstick to control leg position instead of eye
          - topic: 'servo:leg_l_ankle:mv'
            modifier:
              scale: 1.0
          - topic: 'servo:leg_r_ankle:mv'
            modifier:
              scale: -1.0
      BTN_BL+BTN_BR: # Modifiers can be combined: 'only when both buttons are pressed'
        BTN_A:
          - topic: 'tts'
            args: {mgs: 'Both buttons are pressed'}
    modifier_buttons: # Only treat shoulder buttons as modifiers
      - BTN_BL
      - BTN_BR
```

#### How Dynamic Remapping Works

- The `default` mapping is used when no modifier buttons are pressed.
- If a modifier button (or combination) listed in `modifier_buttons` is pressed, the mapping for that combination (e.g., `BTN_BL`, `BTN_BL+BTN_BR`) is used instead, if present.
- The mapping key is a `+`-joined string of pressed modifier button codes, sorted alphabetically.
- If no mapping exists for the current modifier combination, the `default` mapping is used as a fallback.

#### Example Use Cases

- Map `BTN_A` to say "Test Default" by default, but say "Left Shoulder Pressed" when `BTN_BL` is held.
- Map analog axes to different actions or scales depending on which modifier buttons are held.


## Getting Started

1. Connect your controller via Bluetooth or USB.
2. Ensure the `inputs` Python package is installed (`pip install inputs`).
3. Configure your desired button and axis mappings in `config/controller.yml`.
4. Enable the module by setting `enabled: true` in the config.
5. Start the main application. The controller will begin listening for input and publish events as configured.


## Features

- **Dynamic Remapping:** Instantly remap all button and axis actions based on any pressed modifier button or combination, as defined in YAML.
- **Button Mapping:** Map any button to one or more topics with custom arguments.
- **Analog Axis Mapping:** Map analog stick or trigger movement to topics, with support for scaling, inversion, and deadzone filtering.
- **Multiple Actions:** Each button or axis can trigger multiple actions.
- **Deadzone:** Prevents excessive publishing from small analog stick movements. Configurable globally or per-axis.
- **Threaded Listening:** Input is handled in a background thread for responsive control.
- **Modifier Buttons:** Specify any set of buttons as modifiers for context-sensitive remapping.


## Subscriptions

The `Controller` module does not subscribe to topics by default. It only publishes events based on controller input as defined in the configuration.


## Example Use Cases

- Move servos or actuators in real time using analog sticks.
- Trigger speech or sound effects with button presses.
- Combine multiple actions for a single button or axis movement.
- Use modifier buttons to switch between control modes (e.g., normal, alternate, fine control, etc.).
- Remap all controls for a "shift" or "function" mode using any button or combination as a modifier.

## References
- [inputs Python package documentation](https://github.com/zeth/inputs)
- [Linux Gamepad Input Documentation](https://www.kernel.org/doc/html/latest/input/gamepad.html)

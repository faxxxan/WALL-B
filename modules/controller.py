import struct
import threading
import time

from modules.base_module import BaseModule


class Controller(BaseModule):
    """Handles gamepad/joystick input and maps events to pub/sub topics."""

    # Joystick event constants
    JS_EVENT_BUTTON = 0x01
    JS_EVENT_AXIS = 0x02
    JS_EVENT_INIT = 0x80
    JS_EVENT_FORMAT = "IhBB"
    JS_EVENT_SIZE = struct.calcsize(JS_EVENT_FORMAT)

    def __init__(self, **kwargs):
        self.running = False
        self.button_action_map = kwargs.get('button_action_map', {})
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.global_deadzone = kwargs.get('deadzone', 0.0)
        self.global_debounce = kwargs.get('debounce', 800)  # Minimum change threshold
        self.modifier_buttons = set(kwargs.get('modifier_buttons', [])) # Allow alternate mappings when these buttons are held
        self.pressed_buttons = set()
        self.axis_last_value = {}  # Track last value for each axis
        self.axis_last_time = {}   # Track last event time (ms) for each axis
        self.device = kwargs.get('device', "/dev/input/js0") # Required to specify the gamepad device
        if 'button_names' not in kwargs:
            raise ValueError("button_names must be provided in configuration")
        if 'axis_names' not in kwargs:
            raise ValueError("axis_names must be provided in configuration")
        self.button_names = kwargs['button_names']
        self.axis_names = kwargs['axis_names']

    def _get_active_mapping(self):
        """Get the current button map based on pressed modifier buttons."""
        active_mods = sorted(self.pressed_buttons & self.modifier_buttons)
        mapping_key = '+'.join(active_mods) if active_mods else 'default'
        return self.button_action_map.get(mapping_key, self.button_action_map.get('default', {}))

    def setup_messaging(self):
        self.running = True
        self.thread.start()

    def listen(self):
        """Poll the joystick device for input events."""
        self.log("Controller listening for input...")
        while self.running:
            try:
                with open(self.device, "rb") as jsdev:
                    while self.running:
                        evbuf = jsdev.read(self.JS_EVENT_SIZE)
                        if not evbuf:
                            continue
                        time_ms, value, type_, number = struct.unpack(self.JS_EVENT_FORMAT, evbuf)
                        self._handle_js_event(time_ms, value, type_, number)
            except FileNotFoundError:
                self.log(f"No gamepad found at {self.device}. Waiting for connection...", level='warning')
                time.sleep(1)
            except Exception as e:
                self.log(f"Error: {e}", level='error')
                time.sleep(1)

    def _handle_js_event(self, time_ms, value, type_, number):
        """Route joystick events to appropriate handlers."""
        is_init = (type_ & self.JS_EVENT_INIT) != 0
        event_type = type_ & ~self.JS_EVENT_INIT

        topic = None
        args = {}

        if event_type == self.JS_EVENT_BUTTON:
            topic, args = self._handle_button_event(value, number)
        elif event_type == self.JS_EVENT_AXIS:
            topic, args = self._handle_axis_event(value, number)

        self.publish('controller/event', event=(time_ms, value, type_, number, topic, args))

    def _handle_button_event(self, value, number):
        """Handle button press/release events."""
        button = self.button_names.get(number, f'BTN_{number}')
        topic = None
        args = {}

        if value == 1:
            self.pressed_buttons.add(button)
        elif value == 0:
            self.pressed_buttons.discard(button)

        button_map = self._get_active_mapping()
        if button in button_map and value == 1:
            for mapping in button_map[button]:
                topic = mapping.get('topic')
                if not topic:
                    self.log(f"Empty topic for button {button} mapping, skipping.", level='warning')
                    continue
                args = mapping.get('args', {})
                self.publish(topic, **args)
                self.log(f"Published to topic {topic} with args {args} (jsdev)")

        return topic, args

    def _handle_axis_event(self, value, number):
        """Handle axis movement events."""
        axis = self.axis_names.get(number, f'AXIS_{number}')
        topic = None
        args = {}

        button_map = self._get_active_mapping()
        if axis not in button_map:
            return topic, args

        for mapping in button_map[axis]:
            deadzone = mapping.get('deadzone', self.global_deadzone)
            if deadzone > abs(value):
                continue

            debounce = mapping.get('debounce', self.global_debounce)
            now = int(time.monotonic() * 1000)
            last_time = self.axis_last_time.get(axis)

            if last_time is not None and (now - last_time) < debounce:
                continue

            self.axis_last_time[axis] = now
            last_value = self.axis_last_value.get(axis, 0)
            delta = value - last_value
            self.axis_last_value[axis] = value

            topic = mapping.get('topic')
            if not topic:
                self.log(f"Empty topic for axis {axis} mapping, skipping.", level='warning')
                continue

            args = dict(mapping.get('args', {}))
            modifier = mapping.get('modifier')
            if modifier is not None:
                scale = modifier.get('scale', 1.0)
                args['delta'] = delta * scale

            self.publish(topic, **args)
            self.log(f"Published to topic {topic} with args {args} (jsdev)")

        return topic, args

    # Keep public method for backwards compatibility with tests
    def handle_js_event(self, time_ms, value, type_, number):
        """Public wrapper for _handle_js_event (for testing compatibility)."""
        return self._handle_js_event(time_ms, value, type_, number)

    def stop(self):
        """Stop the controller listener thread."""
        self.running = False
        self.thread.join()
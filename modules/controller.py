import threading
import time
from modules.base_module import BaseModule
import yaml

import struct

class Controller(BaseModule):
    def __init__(self, **kwargs):
        self.running = False
        self.button_action_map = kwargs.get('button_action_map', {})
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.global_deadzone = kwargs.get('deadzone', 0.0)
        self.global_debounce = kwargs.get('debounce', 800)  # Minimum change threshold
        self.modifier_buttons = set(kwargs.get('modifier_buttons', []))
        self.pressed_buttons = set()
        self.axis_last_value = {}  # Track last value for each axis
        self.axis_last_time = {}   # Track last event time (ms) for each axis
        self.device = kwargs.get('device', "/dev/input/js0")

    def setup_messaging(self):
        self.running = True
        self.thread.start()

    def listen(self):
        self.log("Controller listening for input...")
        JS_EVENT_FORMAT = "IhBB"
        JS_EVENT_SIZE = struct.calcsize(JS_EVENT_FORMAT)
        while self.running:
            try:
                with open(self.device, "rb") as jsdev:
                    while self.running:
                        evbuf = jsdev.read(JS_EVENT_SIZE)
                        if not evbuf:
                            continue
                        time_ms, value, type_, number = struct.unpack(JS_EVENT_FORMAT, evbuf)
                        # print(f"time={time} value={value} type={type_} number={number}")
                        self.handle_js_event(time_ms, value, type_, number)
            except FileNotFoundError:
                self.log(f"No gamepad found at {self.device}. Waiting for connection...", level='warning')
                time.sleep(1)
            except Exception as e:
                self.log(f"Error reading {self.device}: {e}", level='error')
                time.sleep(1)

    def handle_js_event(self, time_ms, value, type_, number):
        # type_: 0x01 = button, 0x02 = axis, 0x80 = init
        JS_EVENT_BUTTON = 1
        JS_EVENT_AXIS = 0x02
        JS_EVENT_INIT = 0x80

        is_init = (type_ & JS_EVENT_INIT) != 0
        event_type = type_ & ~JS_EVENT_INIT

        # Map button/axis numbers to names as needed for your controller
        button_names = {
            0: 'BTN_A', 1: 'BTN_B', 2: 'BTN_X', 3: 'BTN_Y',
            4: 'BTN_TL', 5: 'BTN_TR', 6: 'BTN_SELECT', 7: 'BTN_START',
            8: 'BTN_MODE', 9: 'BTN_THUMBL', 10: 'BTN_THUMBR'
        }
        axis_names = {
            0: 'ABS_X', 1: 'ABS_Y', 2: 'ABS_Z', 3: 'ABS_RZ',
            4: 'ABS_RX', 5: 'ABS_RY', 6: 'ABS_HAT0X', 7: 'ABS_HAT0Y'
        }
        
        # self.log(f"JS Event: time={time_ms} value={value} type={event_type} number={number} (init={is_init})")

        if event_type == JS_EVENT_BUTTON:
            # self.log(f"JS Button Event: number={number} value={value} (init={is_init})")
            button = button_names.get(number, f'BTN_{number}')
            self.log(f"Button event: {button} value={value} (jsdev)")
            # value: 1=pressed, 0=released
            if value == 1:
                self.pressed_buttons.add(button)
            elif value == 0 and button in self.pressed_buttons:
                self.pressed_buttons.remove(button)

            active_mods = sorted([b for b in self.pressed_buttons if b in self.modifier_buttons])
            mapping_key = '+'.join(active_mods) if active_mods else 'default'
            self.log(f"Active modifiers: {active_mods} (jsdev)")
            button_map = self.button_action_map.get(mapping_key, self.button_action_map.get('default', {}))

            self.log(button)
            if button in button_map and value == 1:
                actions = button_map[button]
                for mapping in actions:
                    topic = mapping.get('topic')
                    if not topic:
                        self.log(f"Empty topic for button {button} mapping, skipping.", level='warning')
                        continue  # Skip empty topic
                    args = mapping.get('args', {})
                    self.publish(topic, **args)
                    self.log(f"Published to topic {topic} with args {args} (jsdev)")

        elif event_type == JS_EVENT_AXIS:
            axis = axis_names.get(number, f'AXIS_{number}')
            # self.log(f"Axis event: {axis} value={value} (jsdev)")
            # value: -32767..32767 for sticks, -1/0/1 for hats
            active_mods = sorted([b for b in self.pressed_buttons if b in self.modifier_buttons])
            mapping_key = '+'.join(active_mods) if active_mods else 'default'
            button_map = self.button_action_map.get(mapping_key, self.button_action_map.get('default', {}))
            self.log(f"Active modifiers: {active_mods} (jsdev)")

            if axis in button_map:
                actions = button_map[axis]
                for mapping in actions:
                    deadzone = mapping.get('deadzone', self.global_deadzone)
                    if deadzone > abs(value):
                        continue  # Skip if within deadzone

                    debounce = mapping.get('debounce', self.global_debounce)  # debounce in ms
                    now = int(time.time() * 1000)  # current time in ms
                    last_time = self.axis_last_time.get(axis, None)

                    # Only allow if enough time has passed
                    if last_time is not None and (now - last_time) < debounce:
                        continue  # Skip if within debounce interval
                    self.axis_last_time[axis] = now
                    last_value = self.axis_last_value.get(axis, 0)
                    delta = value - last_value
                    self.axis_last_value[axis] = value

                    topic = mapping.get('topic')
                    if not topic:
                        continue  # Skip empty topic
                    args = dict(mapping.get('args', {}))  # Copy to avoid mutation
                    modifier = mapping.get('modifier', None)
                    if modifier is not None:
                        scale = modifier.get('scale', 1.0)
                        args['delta'] = delta * scale
                    # self.log(f"Axis {axis} moved to {args.get('delta', value)} (jsdev)")
                    self.publish(topic, **args)
                    self.log(f"Published to topic {topic} with args {args} (jsdev)")
    
    def handle_event(self, event):
        # if event.code == 'ABS_Y':
        # self.log(f"Event: {event.ev_type} {event.code} {event.state}")
        event.modifier_buttons = list(self.pressed_buttons)
        
        # Track pressed/released buttons for modifiers
        if event.ev_type == 'Key':
            if event.state == 1:
                self.pressed_buttons.add(event.code)
            elif event.state == 0 and event.code in self.pressed_buttons:
                self.pressed_buttons.remove(event.code)

        # Determine current mapping set
        mapping_key = None
        # Only consider modifier buttons for mapping key
        active_mods = sorted([b for b in self.pressed_buttons if b in self.modifier_buttons])
        if active_mods:
            mapping_key = '+'.join(active_mods)
        else:
            mapping_key = 'default'
        button_map = self.button_action_map.get(mapping_key, self.button_action_map.get('default', {}))

        # Handle digital button press (use dynamic mapping)
        if (event.ev_type == 'Key' or event.code.startswith('ABS_HAT')) and (event.state == 1 or event.state == -1):
            self.log(f"Button {event.code} pressed")
            button = event.code
            if button in button_map:
                actions = button_map[button]
                for mapping in actions:
                    topic = mapping.get('topic')
                    args = mapping.get('args', {})
                    
                    self.publish(topic, **args)
                    event.topic = topic
                    event.args = args
        # Handle analog stick/trigger movement (use dynamic mapping)
        elif event.ev_type == 'Absolute':
            axis = event.code
            value = event.state
            if axis in button_map:
                actions = button_map[axis]
                for mapping in actions:
                    deadzone = mapping.get('deadzone', self.global_deadzone)
                    if deadzone > abs(value):
                        continue  # Skip if within deadzone

                    debounce = mapping.get('debounce', self.global_debounce)  # debounce in ms
                    now = int(time.time() * 1000)  # current time in ms
                    last_time = self.axis_last_time.get(axis, None)

                    # Only allow if enough time has passed
                    if last_time is not None and (now - last_time) < debounce:
                        continue  # Skip if within debounce interval
                    self.axis_last_time[axis] = now
                    last_value = self.axis_last_value.get(axis, 0)
                    delta = value - last_value
                    self.axis_last_value[axis] = value

                    
                    topic = mapping.get('topic')
                    args = dict(mapping.get('args', {}))  # Copy to avoid mutation
                    modifier = mapping.get('modifier', None)
                    if modifier is not None:
                        scale = modifier.get('scale', 1.0)
                        args['delta'] = delta * scale
                    self.log(f"Axis {axis} moved to {args['delta']}")
                    self.publish(topic, **args)
                    event.topic = topic
                    event.args = args
        self.publish('controller/event', event=event)

    def stop(self):
        self.running = False
        self.thread.join()
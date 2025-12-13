import threading
import time
from modules.base_module import BaseModule
import yaml

try:
    import inputs  # pip install inputs
except ImportError:
    raise ImportError("Please install the 'inputs' package: pip install inputs")

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

    def setup_messaging(self):
        self.running = True
        self.thread.start()

    def listen(self):
        self.log("Controller listening for input...")
        while self.running:
            try:
                events = inputs.get_gamepad()
                for event in events:
                    self.handle_event(event)
            except inputs.UnpluggedError:
                self.log("No gamepad found. Waiting for connection...", level='warning')
                time.sleep(1)
    
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
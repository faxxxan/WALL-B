from PIL import Image, ImageDraw
from modules.display.tft_display import TFTDisplay
import time

class TFTDisplayEye(TFTDisplay):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure colors are stored as tuples
        self.colors = {
            key: tuple(map(int, value.strip('()').split(',')))
            for key, value in kwargs.get('colors', {}).items()
        }
        self.center = (self.disp.width // 2, self.disp.height // 2) # Default center of the display
        self.radius = 50
        self.pos = self.center
        if kwargs.get('test_on_boot'):
            self.init_eye()

    def setup_messaging(self):
        self.subscribe('eye', self.eye)
        self.subscribe('eye/look', self.look)
        self.subscribe('eye/blink', self.blink)
        self.subscribe('eye/move', self.move_eye)

    def init_eye(self):
        self.draw_image('makerforge_bl.png')
        time.sleep(2)
        img = None
        
        # Increase radius from 0 to 70 in steps of 5
        for x in range(0, self.radius, 5):
            img = self.draw_halo(
                ring_radius=x,
                color=self.colors['blue'],
                glow_spread=10
            )
        # increase glow spread from 10 to 30 in steps of 5
        for x in range(10, 30, 2):
            img = self.draw_halo(
                color=self.colors['blue'],
                glow_spread=x
            )
        self.img = self.eye('blue')
        time.sleep(3)
        self.blink()
        print("TFT display test completed")

    def eye(self, color):
        # print(f"Eye color: {color}")
        # If color doesn't exist, throw exception
        if color not in self.colors:
            raise ValueError(f"Color '{color}' not found in available colors.")
        # Access the color as a tuple
        return self.draw_halo(
            ring_radius=self.radius,
            ring_thickness=10,
            color=self.colors[color]
        )
    
    def move_eye(self, axis, delta):
        delta_x = delta if axis == 'x' else 0
        delta_y = delta if axis == 'y' else 0
        new_x = max(0, min(self.disp.width, self.pos[0] + delta_x))
        new_y = max(0, min(self.disp.height, self.pos[1] + delta_y))
        self.pos = (new_x, new_y)
        self.img = self.draw_halo(
            ring_radius=self.radius,
            ring_thickness=10,
            color=self.colors['blue']
        )
        
    def look(self, coordinates=None):
        if coordinates is None:
            coordinates = (self.disp.width // 2, self.disp.height // 2)
        current_center = self.center
        target_center = coordinates

        # steps = distance between current and target divided by 10
        steps = max(
            abs(target_center[0] - current_center[0]),
            abs(target_center[1] - current_center[1])
        ) // 10 or 1
        
        delay = 0.01  # seconds per step

        for i in range(1, steps + 1):
            interp_center = (
                int(current_center[0] + (target_center[0] - current_center[0]) * i / steps),
                int(current_center[1] + (target_center[1] - current_center[1]) * i / steps)
            )
            self.center = interp_center
            self.img = self.draw_halo(
                ring_radius=self.radius,
                ring_thickness=10,
                color=self.colors['blue']
            )
            time.sleep(delay)
        self.center = target_center

    def draw_halo(self, color, ring_radius=50, ring_thickness=10, glow_layers=12, glow_spread=30):
        disp = self.disp
        center = self.center
        glow_image = Image.new("RGBA", (disp.width, disp.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow_image)

        for i in range(glow_layers):
            spread = int(i * glow_spread / glow_layers)
            alpha = int(255 * (1 - i / glow_layers) ** 2 * 0.5)
            glow_color = (color[0], color[1], color[2], alpha)

            outer_radius = ring_radius + ring_thickness // 2 + spread
            inner_radius = ring_radius - ring_thickness // 2 - spread

            outer_bbox = [
                center[0] - outer_radius,
                center[1] - outer_radius,
                center[0] + outer_radius,
                center[1] + outer_radius
            ]
            draw.ellipse(outer_bbox, outline=glow_color, width=3)

            if inner_radius > 0:
                inner_bbox = [
                    center[0] - inner_radius,
                    center[1] - inner_radius,
                    center[0] + inner_radius,
                    center[1] + inner_radius
                ]
                draw.ellipse(inner_bbox, outline=glow_color, width=3)

        ring_bbox = [
            center[0] - ring_radius - 2,
            center[1] - ring_radius - 2,
            center[0] + ring_radius + 2,
            center[1] + ring_radius + 2
        ]
        draw.ellipse(ring_bbox, outline=(color[0], color[1], color[2], 255), width=ring_thickness)

        final_image = Image.new("RGB", (disp.width, disp.height), "BLACK")
        final_image.paste(glow_image, (0, 0), glow_image)
        disp.ShowImage(final_image)
        return final_image

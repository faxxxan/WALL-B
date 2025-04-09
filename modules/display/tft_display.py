#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from modules.display.lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont, ImageEnhance
from modules.base_module import BaseModule

class TFTDisplay(BaseModule):
    red = (255, 32, 32)
    blue = (0, 245, 255)
    green = (0, 255, 180)
    purple = (255, 0, 255)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)
    dark_gray = (64, 64, 64)
    
    def __init__(self, **kwargs):
        try:
            # Open SPI bus
            spi = SPI.SpiDev(kwargs.get('bus'), kwargs.get('device'))
            spi.max_speed_hz = 10000000
            
            # Display with hardware SPI:
            ''' Warning!!! Don't create multiple display objects!!! '''
            self.disp = LCD_1inch28.LCD_1inch28(spi=spi, spi_freq=10000000, rst=kwargs.get('rst_pin'), dc=kwargs.get('dc_pin') , bl=kwargs.get('bl_pin'))
            self.clear_display()
            if kwargs.get('test_on_boot'):
                self.init_eye()
           
        except Exception as e:
            logging.error(f"Failed to initialize TFT display: {e}")
    
    def setup_messaging(self):
        # Set subscribers
        self.subscribe('eye', self.eye)
            
    def init_eye(self):
        self.clear_display()
        time.sleep(1)
        self.draw_image('makerforge_bl.png')
        time.sleep(2)
        for x in range(20, 70, 5):
            self.draw_halo(
                ring_radius=x,
                ring_thickness=10,
                color=self.red,
                glow_layers=12,
                glow_spread=30
            )
        
        current_img = None
        for x in range(10, 15):
            current_img = self.draw_halo(
                ring_radius=70,
                ring_thickness=x,
                color=self.green,
                glow_layers=12,
                glow_spread=30
            )
        
        time.sleep(3)
        
        # 70 radius, thickness 2
        for x in range(15, 2, -1):
            self.draw_halo(
                ring_radius=70,
                ring_thickness=x,
                color=self.green,
                glow_layers=12,
                glow_spread=30
            )
        time.sleep(1)
        # 70 radius, thickness 30
        for x in range(2, 30, 2):
            self.draw_halo(
                ring_radius=70,
                ring_thickness=x,
                color=self.green,
                glow_layers=12,
                glow_spread=30
            )
        
        time.sleep(1)
        
        # 70 radius, thickness 10, glow spread 10
        for x in range(30, 10, -2):
            self.draw_halo(
                ring_radius=70,
                ring_thickness=10,
                color=self.green,
                glow_layers=12,
                glow_spread=x
            )
        time.sleep(1)
        
        # 70 radius, thickness 10, glow spread 30
        for x in range(10, 30, 2):
            current_img = self.draw_halo(
                ring_radius=70,
                ring_thickness=10,
                color=self.green,
                glow_layers=12,
                glow_spread=x
            )
        time.sleep(.5)
        # blue
        current_img = self.draw_halo(
            ring_radius=70,
            ring_thickness=10,
            color=self.blue,
            glow_layers=12,
            glow_spread=30
        )
        time.sleep(.5)
        
        # gray
        current_img = self.draw_halo(
            ring_radius=70,
            ring_thickness=10,
            color=self.gray,
            glow_layers=12,
            glow_spread=30
        )
        time.sleep(.5)
        # purple
        current_img = self.draw_halo(
            ring_radius=70,
            ring_thickness=10,
            color=self.purple,
            glow_layers=12,
            glow_spread=30
        )
        time.sleep(.5)
        # yellow
        current_img = self.draw_halo(
            ring_radius=70,
            ring_thickness=10,
            color=self.yellow,
            glow_layers=12,
            glow_spread=30
        )
        time.sleep(.5)
        # white
        current_img = self.draw_halo(
            ring_radius=70,
            ring_thickness=10,
            color=self.white,
            glow_layers=12,
            glow_spread=30
        )
        time.sleep(.5)
        # blue
        current_img = self.draw_halo(
            ring_radius=70,
            ring_thickness=10,
            color=self.blue,
            glow_layers=12,
            glow_spread=30
        )
        
        time.sleep(3)
        
        self.blink_image(
            image=current_img,
            off_time=0.15
        )

        print("TFT display test completed")

    def eye(self, color):
        if color == 'red':
            color = self.dark_gray
        elif color == 'blue':
            color = self.blue
        elif color == 'green':
            color = self.green
        
        self.draw_halo(
                ring_radius=70,
                ring_thickness=15,
                color=color,
                glow_layers=12,
                glow_spread=30)
        
    def clear_display(self):
        disp = self.disp
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()
        # Set the backlight to 100
        disp.bl_DutyCycle(50)
        return disp

    def draw_image(self, img):
        disp = self.disp
        image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
        image = Image.open(os.getcwd() + '/modules/display/images/' + img)
        new_image = image.resize((disp.width, disp.height))
        new_image = new_image.rotate(-90.0)
        disp.ShowImage(new_image)
        
    def draw_circle(self, radius, thickness, color, glow, glow_radius):
        disp = self.disp
        
        # Create blank image for drawing.
        image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(image1)

        # Outer glow 
        draw.ellipse((radius - glow_radius, radius - glow_radius, (disp.width - radius + glow_radius), (disp.width - radius + glow_radius)), fill = glow)
        # Eye
        draw.ellipse(((radius), (radius), (disp.width - radius), (disp.width - radius)), fill = color)
        # Inner glow
        draw.ellipse(((radius + thickness), (radius + thickness), (disp.width - radius - thickness), (disp.width - radius - thickness)), fill = glow)
        # Center
        draw.ellipse(((radius + thickness + glow_radius), (radius + thickness + glow_radius), (disp.width - radius - thickness - glow_radius), (disp.width - radius - thickness - glow_radius)), fill = (0, 46, 5))

        disp.ShowImage(image1)
        

    def draw_halo(self, ring_radius, ring_thickness, color, glow_layers=10, glow_spread=20):
        disp = self.disp
        center = (disp.width // 2, disp.width // 2)

        # Create an RGBA image to allow transparency and glow effect
        glow_image = Image.new("RGBA", (disp.width, disp.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow_image)

        # Total glow spread includes both inward and outward
        for i in range(glow_layers):
            # Spread amount relative to center of ring
            spread = int(i * glow_spread / glow_layers)
            alpha = int(255 * (1 - i / glow_layers) ** 2 * 0.5)
            glow_color = (color[0], color[1], color[2], alpha)

            outer_radius = ring_radius + ring_thickness // 2 + spread
            inner_radius = ring_radius - ring_thickness // 2 - spread

            # Outer glow
            outer_bbox = [
                center[0] - outer_radius,
                center[1] - outer_radius,
                center[0] + outer_radius,
                center[1] + outer_radius
            ]
            draw.ellipse(outer_bbox, outline=glow_color, width=3)

            # Inner glow
            if inner_radius > 0:
                inner_bbox = [
                    center[0] - inner_radius,
                    center[1] - inner_radius,
                    center[0] + inner_radius,
                    center[1] + inner_radius
                ]
                draw.ellipse(inner_bbox, outline=glow_color, width=3)

        # Main ring (added 2 to remove black border)
        ring_bbox = [
            center[0] - ring_radius - 2,
            center[1] - ring_radius - 2,
            center[0] + ring_radius + 2,
            center[1] + ring_radius + 2
        ]
        draw.ellipse(ring_bbox, outline=(color[0], color[1], color[2], 255), width=ring_thickness)

        # Composite on black background and show
        final_image = Image.new("RGB", (disp.width, disp.height), "BLACK")
        final_image.paste(glow_image, (0, 0), glow_image)
        disp.ShowImage(final_image)
        return final_image

    def blink_image(self, image, off_time=0.2):
        disp = self.disp
        image1 = Image.new("RGBA", (disp.width, disp.height), "BLACK")
        disp.ShowImage(image1)
        time.sleep(off_time)
        disp.ShowImage(image)

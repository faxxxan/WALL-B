#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import logging
import spidev as SPI
from PIL import Image
from modules.base_module import BaseModule
from modules.display.lib import LCD_1inch28

class TFTDisplay(BaseModule):
    def __init__(self, **kwargs):
        self.rotation = kwargs.get('rotation', 0)
        try:
            spi = SPI.SpiDev(kwargs.get('bus'), kwargs.get('device'))
            spi.max_speed_hz = 10000000
            self.disp = LCD_1inch28.LCD_1inch28(
                spi=spi, spi_freq=10000000, rst=kwargs.get('rst_pin'),
                dc=kwargs.get('dc_pin'), bl=kwargs.get('bl_pin')
            )
            self.clear_display()
            blank_image = Image.new("RGBA", (self.disp.width, self.disp.height), "BLACK")
            self.disp.ShowImage(blank_image)
            
            if kwargs.get('test_on_boot'):
                self.draw_image('makerforge_bl.png')
        except Exception as e:
            logging.error(f"Failed to initialize TFT display: {e}")

    def setup_messaging(self):
        pass  # Placeholder for messaging setup

    def clear_display(self):
        disp = self.disp
        disp.Init()
        disp.clear()
        disp.bl_DutyCycle(50)
        return disp

    def draw_image(self, img):
        disp = self.disp
        image = Image.open(os.getcwd() + '/modules/display/images/' + img)
        new_image = image.resize((disp.width, disp.height)).rotate(self.rotation)
        disp.ShowImage(new_image)

    def blink(self, image, off_time=0.2):
        disp = self.disp
        blank_image = Image.new("RGBA", (disp.width, disp.height), "BLACK")
        disp.ShowImage(blank_image)
        time.sleep(off_time)
        disp.ShowImage(image)

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


class Ufo:
    def __init__(
        self,
        sw_0_pin=9,
        sw_2_pin=7,
        scl_pin=15,
        sda_pin=14,
        i2c_freq=400000,
        oled_w=128,
        oled_h=64,
        font_size=8,
        ufo_text="<=>"
    ):
        self.sw_0 = Pin(sw_0_pin, Pin.IN, Pin.PULL_UP)
        self.sw_2 = Pin(sw_2_pin, Pin.IN, Pin.PULL_UP)
        self.i2c = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)
        self.oled = SSD1306_I2C(oled_w, oled_h, self.i2c)
        self.ufo_w = font_size * len(ufo_text)
        self.x = (oled_w // 2) - (self.ufo_w // 2)
        self.y = oled_h - font_size
        self.oled_w = oled_w
        self.oled_h = oled_h
        self.ufo_text = ufo_text
    
    def run(self):
        while True:
            if self.sw_2.value() == 0:      # hold to draw
                self.move_left()
            
            if self.sw_0.value() == 0:
                self.move_right()
            
            self.oled.fill(0)
            self.oled.text(self.ufo_text, self.x, self.y, 1)
            self.oled.show()
    
    def move_left(self):
        if self.x > 0:
            self.x -= 1
    
    def move_right(self):
        if self.x < self.oled_w - self.ufo_w:
            self.x += 1
    
    


if __name__ == "__main__":
    ufo = Ufo()
    ufo.run()
from machine import Pin, I2C

from ssd1306 import SSD1306_I2C

from config import Pins, Display as DisplayConfig


class Display:
    """OLED wrapper. The rest of the project never touches I2C or ssd1306 directly."""

    def __init__(self):
        i2c = I2C(
            DisplayConfig.I2C_ID,
            scl=Pin(Pins.OLED_SCL),
            sda=Pin(Pins.OLED_SDA),
            freq=DisplayConfig.I2C_FREQ,
        )
        self._oled = SSD1306_I2C(
            DisplayConfig.WIDTH,
            DisplayConfig.HEIGHT,
            i2c,
            addr=DisplayConfig.I2C_ADDRESS,
        )

    def clear(self):
        self._oled.fill(0)

    def text(self, string, x, y):
        self._oled.text(string, x, y)

    def show(self):
        self._oled.show()
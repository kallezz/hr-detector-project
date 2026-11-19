from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time


class SineWaveDisplay:
    FILE_NAMES = [
        "/data/sinewave_250Hz_01.txt",
        "/data/sinewave_250Hz_02.txt",
        "/data/sinewave_250Hz_03.txt",
    ]
    SAMPLES_TO_READ = 500
    MAX_LINES = 8
    DELAY = 0.02

    def __init__(self, file_num):
        i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled = SSD1306_I2C(128, 64, i2c)

        self.file_name = self.FILE_NAMES[file_num]
        self.min_val = None
        self.max_val = None
        self.values = []
    
    def _update_calibration(self, sample):
        if self.min_val is None:
            self.min_val = sample
            self.max_val = sample
        elif sample < self.min_val:
            self.min_val = sample
        elif sample > self.max_val:
            self.max_val = sample

    def _calibrate(self):
        data = Filefifo(10, name=self.file_name)
        for _ in range(self.SAMPLES_TO_READ):
            self._update_calibration(data.get())
    
    def _scale(self, sample):
        return (sample - self.min_val) / (self.max_val - self.min_val) * 100
    
    def _add_line(self, scaled_value):
        self.values.append(scaled_value)
        if len(self.values) > self.MAX_LINES:
            self.values.pop(0)

    def _draw(self):
        self.oled.fill(0)
        for i, value in enumerate(self.values):
            self.oled.text(str(int(value)), 0, i * 8, 1)
            bar_w = int(value * 0.85)
            self.oled.fill_rect(35, i * 8, bar_w, 6, 1)
        self.oled.show()

    def run(self):
        self._calibrate()

        while True:
            data = Filefifo(10, name=self.file_name)
            self.values = []

            for _ in range(self.SAMPLES_TO_READ):
                scaled = self._scale(data.get())
                self._add_line(scaled)
                self._draw()
                time.sleep(self.DELAY)


if __name__ == "__main__":
    print("Select file 0, 1 or 2:")
    file_num = int(input())
    sine_display = SineWaveDisplay(file_num)
    sine_display.run()

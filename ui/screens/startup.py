import math
import random
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


class Startup:
    OLED_W = 128
    OLED_H = 64

    def __init__(
        self,
        scl_pin=15,
        sda_pin=14,
        i2c_freq=400000,
        heart_scale=1.4,
        heart_gap=0.6,      # bigger = wider opening at the bottom
        pulses_per_side=2,
        margin=6,           # clear space between pulses and the heart
        batch=1,            # segments drawn per display refresh
        frame_ms=0,         # extra delay per refresh
    ):
        self.i2c = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)
        self.oled = SSD1306_I2C(self.OLED_W, self.OLED_H, self.i2c)
        self.batch = batch
        self.frame_ms = frame_ms
        self.heart_scale = heart_scale
        self.heart_gap = heart_gap
        self.pulses_per_side = pulses_per_side
        self.margin = margin

    @staticmethod
    def _add(pts, x, y, step=4):
        """Append a point, filling in intermediate points so the drawing speed stays even."""
        if pts:
            px, py = pts[-1]
            n = max(abs(x - px), abs(y - py)) // step
            for k in range(1, n):
                pts.append((int(px + (x - px) * k / n), int(py + (y - py) * k / n)))
        pts.append((x, y))

    def _heart(self):
        s = self.heart_scale
        cx = self.OLED_W // 2
        g = self.heart_gap
        steps = 48
        pts = []
        for i in range(steps + 1):
            t = math.pi + g + (2 * math.pi - 2 * g) * i / steps
            hx = 16 * math.sin(t) ** 3
            hy = (13 * math.cos(t) - 5 * math.cos(2 * t)
                  - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((int(cx + hx * s), int(32 - (hy + 2.5) * s)))
        return pts

    def _pulses(self, pts, y, zone_start, zone_end):
        """Add random ECG-style pulses, all inside [zone_start, zone_end]."""
        n = self.pulses_per_side
        slot = (zone_end - zone_start) // n
        for i in range(n):
            px = zone_start + i * slot + random.randint(0, max(0, slot - 8))
            h = random.randint(5, 12)
            if random.randint(0, 1):
                h = -h
            self._add(pts, px, y)
            self._add(pts, px + 2, y - h)
            self._add(pts, px + 4, y + h // 2)
            self._add(pts, px + 6, y)

    def _build_path(self):
        heart = self._heart()
        y = heart[0][1]  # baseline = height where the heart opens
        heart_left = min(p[0] for p in heart)
        heart_right = max(p[0] for p in heart)
        m = self.margin

        pts = []

        # Left side: pulses only to the left of the heart
        self._add(pts, 0, y)
        self._pulses(pts, y, 0, heart_left - m)
        self._add(pts, heart[0][0], y)

        # Heart
        for x, hy in heart[1:]:
            self._add(pts, x, hy)

        # Right side: pulses only to the right of the heart
        self._add(pts, heart_right + m, y)
        self._pulses(pts, y, heart_right + m, self.OLED_W - 1)
        self._add(pts, self.OLED_W - 1, y)

        return pts

    def run(self):
        path = self._build_path()  # new random pulses every run

        self.oled.fill(0)
        self.oled.show()

        for i in range(1, len(path)):
            x0, y0 = path[i - 1]
            x1, y1 = path[i]
            self.oled.line(x0, y0, x1, y1, 1)
            if i % self.batch == 0:
                self.oled.show()
                if self.frame_ms:
                    time.sleep_ms(self.frame_ms)

        self.oled.show()
        time.sleep(1)
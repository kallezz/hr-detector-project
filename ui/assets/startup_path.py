import math
import random

from config import Display, StartupAnim as Anim


class StartupPath:
    """Builds the point list for the ECG line and heart. Pure logic, no hardware."""

    # Coefficients of the standard parametric heart curve (mathematical, not tunable)
    _HEART_X_COEFF = 16
    _HEART_Y_COEFFS = (13, -5, -2, -1)

    def build(self):
        """Return a new path with random pulses: left pulses, heart, right pulses."""
        heart = self._heart()
        baseline = heart[0][1]
        heart_left = min(p[0] for p in heart)
        heart_right = max(p[0] for p in heart)
        pts = []
        self._add(pts, 0, baseline)
        self._pulses(pts, baseline, 0, heart_left - Anim.MARGIN)
        self._add(pts, heart[0][0], baseline)
        for x, y in heart[1:]:
            self._add(pts, x, y)
        self._add(pts, heart_right + Anim.MARGIN, baseline)
        self._pulses(pts, baseline, heart_right + Anim.MARGIN, Display.WIDTH - 1)
        self._add(pts, Display.WIDTH - 1, baseline)
        return pts

    @staticmethod
    def _add(pts, x, y):
        """Append a point, filling in intermediate points so drawing speed stays even."""
        if pts:
            px, py = pts[-1]
            n = max(abs(x - px), abs(y - py)) // Anim.INTERPOLATION_STEP
            for k in range(1, n):
                pts.append((int(px + (x - px) * k / n), int(py + (y - py) * k / n)))
        pts.append((x, y))

    def _heart(self):
        """Return the heart outline as a list of (x, y) points."""
        gap = Anim.HEART_GAP
        pts = []
        for i in range(Anim.HEART_STEPS + 1):
            t = math.pi + gap + (2 * math.pi - 2 * gap) * i / Anim.HEART_STEPS
            pts.append(self._heart_point(t))
        return pts

    def _heart_point(self, t):
        """Screen position of the heart curve at angle t."""
        a, b, c, d = self._HEART_Y_COEFFS
        hx = self._HEART_X_COEFF * math.sin(t) ** 3
        hy = a * math.cos(t) + b * math.cos(2 * t) + c * math.cos(3 * t) + d * math.cos(4 * t)
        x = Display.WIDTH // 2 + hx * Anim.HEART_SCALE
        y = Display.HEIGHT // 2 - (hy + Anim.HEART_Y_OFFSET) * Anim.HEART_SCALE
        return int(x), int(y)

    def _pulses(self, pts, y, zone_start, zone_end):
        """Add random ECG-style pulses, all inside [zone_start, zone_end]."""
        count = Anim.PULSES_PER_SIDE
        slot = (zone_end - zone_start) // count
        spread = max(0, slot - Anim.PULSE_WIDTH - Anim.PULSE_SLOT_MARGIN)
        step = Anim.PULSE_WIDTH // 3
        for i in range(count):
            px = zone_start + i * slot + random.randint(0, spread)
            h = random.randint(Anim.PULSE_MIN_HEIGHT, Anim.PULSE_MAX_HEIGHT)
            if random.randint(0, 1):
                h = -h
            self._add(pts, px, y)
            self._add(pts, px + step, y - h)
            self._add(pts, px + 2 * step, y + h // 2)
            self._add(pts, px + 3 * step, y)
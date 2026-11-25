from time import ticks_ms, ticks_diff

from config import Input, ScreenId, StartupAnim as Anim
from ui.screen import Screen
from ui.assets.startup_path import StartupPath


class StartupScreen(Screen):
    """Boot animation: an ECG line draws itself into a heart, then the menu opens."""

    def __init__(self):
        self._path_builder = StartupPath()
        self._path = []
        self._reached = 0          # last path point that should be visible
        self._drawn = 0            # last path point already drawn
        self._needs_clear = True
        self._finished_ms = None

    def enter(self):
        """Build a fresh random path and restart the animation."""
        self._path = self._path_builder.build()
        self._reached = 0
        self._drawn = 0
        self._needs_clear = True
        self._finished_ms = None

    def handle_input(self, event):
        """Any press skips the animation."""
        if event == Input.PRESS:
            return ScreenId.MENU
        return None

    def update(self):
        """Reveal more of the path, then hold briefly and open the menu."""
        last = len(self._path) - 1
        if self._reached < last:
            self._reached = min(self._reached + Anim.SEGMENTS_PER_FRAME, last)
        elif self._finished_ms is None:
            self._finished_ms = ticks_ms()
        elif ticks_diff(ticks_ms(), self._finished_ms) >= Anim.HOLD_MS:
            return ScreenId.MENU
        return None

    def draw(self, display):
        """Draw only the new segments; the earlier ones are still on screen."""
        if self._needs_clear:
            display.clear()
            self._needs_clear = False
        elif self._drawn == self._reached:
            return
        for i in range(self._drawn + 1, self._reached + 1):
            x0, y0 = self._path[i - 1]
            x1, y1 = self._path[i]
            display.line(x0, y0, x1, y1)
        self._drawn = self._reached
        display.show()
"""Base class that every screen inherits from."""

from hardware.input_events import InputEvent
from ui import layout
from ui.screen_ids import ScreenId

class Screen:

    TITLE = ""

    def __init__(self, display, navigator):
        self._display = display
        self._navigator = navigator

    def enter(self):


    def update(self):
       return False

    def handle_input(self, event):
        if event == InputEvent.PRESS:
            self._navigator.go_to(ScreenId.MENU)

    def draw(self):
        self._display.draw_text(
            self.TITLE, layout.SCREEN_TEXT_X, layout.SCREEN_TITLE_Y
        )
        self._display.draw_text(
            layout.BACK_HINT_TEXT, layout.SCREEN_TEXT_X, layout.SCREEN_HINT_Y
        )


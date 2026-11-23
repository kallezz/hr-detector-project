from config import Input, Ui, Display
from ui.screen import Screen


class MenuScreen(Screen):
    """Main menu: turn to move the selection, press to open a screen."""

    def __init__(self):
        self._selected = 0

    def handle_input(self, event):
        if event == Input.RIGHT:
            self._selected = (self._selected + 1) % len(Ui.MENU_ITEMS)
        elif event == Input.LEFT:
            self._selected = (self._selected - 1) % len(Ui.MENU_ITEMS)
        elif event == Input.PRESS:
            return Ui.MENU_TARGETS[self._selected]
        return None

    def draw(self, display):
        display.clear()
        for index, item in enumerate(Ui.MENU_ITEMS):
            cursor = Ui.MENU_CURSOR if index == self._selected else " "
            display.text(cursor + item, Ui.MENU_X, index * Display.LINE_HEIGHT)
        display.show()
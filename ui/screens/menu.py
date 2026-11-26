from config import Input, Ui, Display
from ui.screen import Screen
from ui.assets.icons import MenuIcons


class MenuScreen(Screen):
    """Main menu: turn to move the selection, press to open a screen."""

    def __init__(self):
        self._selected = 0
        self._icons = MenuIcons()
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
            y = index * Display.LINE_HEIGHT
            if index == self._selected:
                display.text(Ui.MENU_CURSOR, Ui.MENU_X, y)
            display.blit(self._icons.for_screen(Ui.MENU_TARGETS[index]), Ui.MENU_ICON_X, y)
            display.text(item, Ui.MENU_TEXT_X, y)
        display.show()
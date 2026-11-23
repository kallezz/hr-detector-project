from config import Input, ScreenId
from ui.screen import Screen


class PlaceholderScreen(Screen):
    """Temporary screen for features not built yet. Press to return to the menu."""

    def __init__(self, title):
        self._title = title

    def handle_input(self, event):
        if event == Input.PRESS:
            return ScreenId.MENU
        return None

    def draw(self, display):
        display.clear()
        display.text(self._title, 0, 0)
        display.show()
from config import ScreenId, Ui
from hardware.display import Display
from hardware.encoder import Encoder
from ui.app import App
from ui.screens.menu import MenuScreen
from ui.screens.placeholder import PlaceholderScreen


def build_screens():
    """Create all screens. Placeholders stand in for the ones not written yet."""
    screens = {ScreenId.MENU: MenuScreen()}
    for screen_id, title in zip(Ui.MENU_TARGETS, Ui.MENU_ITEMS):
        screens[screen_id] = PlaceholderScreen(title)
    return screens


def main():
    """Entry point: build the objects, pass them in, start the app."""
    encoder = Encoder()
    display = Display()
    App(encoder, display, build_screens()).run()


main()

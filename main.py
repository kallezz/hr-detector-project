from config import ScreenId, Ui
from hardware.display import Display
from hardware.encoder import Encoder
from storage.history_store import HistoryStore
from ui.app import App
from ui.screens.startup import StartupScreen
from ui.screens.menu import MenuScreen
from ui.screens.placeholder import PlaceholderScreen
from ui.screens.heart_rate import HeartRateScreen
from ui.screens.hrv import HrvScreen
from ui.screens.history import HistoryScreen


def build_screens():
    screens = {
        ScreenId.STARTUP: StartupScreen(),
        ScreenId.MENU: MenuScreen(),
        ScreenId.HEART_RATE: HeartRateScreen(),
        ScreenId.HRV: HrvScreen(),
        ScreenId.HISTORY: HistoryScreen(HistoryStore()),
    }
    for screen_id, title in zip(Ui.MENU_TARGETS, Ui.MENU_ITEMS):
        if screen_id not in screens:
            screens[screen_id] = PlaceholderScreen(title)
    return screens


def main():
    encoder = Encoder()
    display = Display()
    App(encoder, display, build_screens()).run()


main()
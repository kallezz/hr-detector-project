
import config
from input_events import InputEvent


class ScreenId:
    MENU = 0
    MEASURE_HR = 1
    HRV_ANALYSIS = 2
    KUBIOS = 3
    HISTORY = 4


class Screen:

    TITLE = ""

    def __init__(self, display, navigator):
        self._display = display
        self._navigator = navigator

    def on_enter(self):

    def handle_event(self, event):
        if event == InputEvent.PRESS:
            self._navigator.go_to(ScreenId.MENU)

    def draw(self):
        self._display.draw_text(
            self.TITLE, config.SCREEN_TEXT_X, config.SCREEN_TITLE_Y
        )
        self._display.draw_text(
            config.BACK_HINT_TEXT, config.SCREEN_TEXT_X, config.SCREEN_HINT_Y
        )


class MenuScreen(Screen):

    def __init__(self, display, navigator, entries):
        super().__init__(display, navigator)
        self._entries = entries
        self._selected_index = 0

    def handle_event(self, event):
        if event == InputEvent.ROTATE_CW:
            self._selected_index = (self._selected_index + 1) % len(self._entries)
        elif event == InputEvent.ROTATE_CCW:
            self._selected_index = (self._selected_index - 1) % len(self._entries)
        elif event == InputEvent.PRESS:
            _, screen_id = self._entries[self._selected_index]
            self._navigator.go_to(screen_id)

    def draw(self):
        for index, (label, _) in enumerate(self._entries):
            text_y = (
                config.MENU_TOP_Y
                + index * config.MENU_ROW_HEIGHT
                + config.HIGHLIGHT_PADDING_Y
            )
            is_selected = index == self._selected_index
            self._display.draw_text(label, config.MENU_TEXT_X, text_y, is_selected)


class MeasureHrScreen(Screen):

    TITLE = "Measure HR"


class HrvAnalysisScreen(Screen):

    TITLE = "HRV analysis"


class KubiosScreen(Screen):

    TITLE = "Kubios"


class HistoryScreen(Screen):

    TITLE = "History"

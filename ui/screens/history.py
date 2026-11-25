from config import Display as DisplayConfig, Input, ScreenId, Storage, Ui
from ui.screen import Screen
from storage.history_store import HistoryStore


class HistoryScreen(Screen):
    def init(self):
        super().init()
        self._store = HistoryStore()
        self._records = []
        self._selected_index = 0
        self._open_record = None  # the measurement on the detail page

    def enter(self):
        self._records = self._store.load()[:Ui.HISTORY_RECORD_ROWS]
        self._selected_index = 0
        self._open_record = None

    def handle_input(self, event):
        if self._open_record is not None:
            return self._handle_detail_input(event)
        return self._handle_list_input(event)

    def draw(self, display):
        display.clear()
        if self._open_record is not None:
            self._draw_detail(display)
        else:
            self._draw_list(display)
        display.show()

    def _handle_detail_input(self, event):
        """On the detail page a press goes back to the list."""
        if event == Input.PRESS:
            self._open_record = None
        return None

    def _handle_list_input(self, event):
        row_count = len(self._row_labels())
        if event == Input.RIGHT:
            self._selected_index = (self._selected_index + 1) % row_count
        elif event == Input.LEFT:
            self._selected_index = (self._selected_index - 1) % row_count
        elif event == Input.PRESS:
            return self._press_selected_row()
        return None

    def _press_selected_row(self):
        if self._selected_index == len(self._records):
            return ScreenId.MENU
        self._open_record = self._records[self._selected_index]
        return None

    def _row_labels(self):
        """The list rows: one time per measurement, then the Back row."""
        labels = [record.get(Storage.FIELD_TIME, "") for record in self._records]
        labels.append(Ui.HISTORY_BACK_LABEL)
        return labels

    def _draw_list(self, display):
        first_row = 0
        if not self._records:
            display.text(Ui.HISTORY_EMPTY_TEXT, Ui.HISTORY_TEXT_X, 0)
            first_row = 1
        for index, label in enumerate(self._row_labels()):
            row_y = (index + first_row) * Ui.HISTORY_ROW_HEIGHT
            display.text(label, Ui.HISTORY_TEXT_X, row_y)
            if index == self._selected_index:
                underline_y = row_y + DisplayConfig.LINE_HEIGHT
                display.line(
                    Ui.HISTORY_TEXT_X, underline_y,
                    Ui.HISTORY_LINE_END_X, underline_y,
                )

    def _draw_detail(self, display):
        record = self._open_record
        display.text(record.get(Storage.FIELD_TIME, ""), Ui.HISTORY_TEXT_X, 0)
        row = 1
        for label, key, number_format in Ui.HISTORY_FIELDS:
            value = record.get(key)
            if value is None:
                continue
            line = Ui.HISTORY_FIELD_FORMAT.format(label, number_format.format(value))
            display.text(line, Ui.HISTORY_TEXT_X, row * DisplayConfig.LINE_HEIGHT)
            row += 1
        hint_y = DisplayConfig.HEIGHT - DisplayConfig.LINE_HEIGHT
        display.text(Ui.HISTORY_HINT_TEXT, Ui.HISTORY_TEXT_X, hint_y)
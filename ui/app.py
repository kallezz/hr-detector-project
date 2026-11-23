from time import sleep_ms
from config import Input, ScreenId, Ui, Encoder as EncoderConfig


class App:
    _TURN_TO_EVENT = {
        EncoderConfig.TURN_LEFT: Input.LEFT,
        EncoderConfig.TURN_RIGHT: Input.RIGHT,
    }

    def __init__(self, encoder, display, screens):
        self._encoder = encoder
        self._display = display
        self._screens = screens          # dict: ScreenId -> Screen
        self._current = None
        self._switch_to(ScreenId.MENU)

    def run(self):
        while True:
            self._step()
            sleep_ms(Ui.FRAME_INTERVAL_MS)

    def _step(self):
        next_id = self._handle_inputs()
        if next_id is None:
            next_id = self._current.update()
        if next_id is not None:
            self._switch_to(next_id)
        self._current.draw(self._display)

    def _handle_inputs(self):
        """Pass queued input events to the screen; stop at the first switch."""
        for event in self._read_events():
            next_id = self._current.handle_input(event)
            if next_id is not None:
                return next_id
        return None

    def _read_events(self):
        """Convert encoder state into Input events (no IRQ work happens here)."""
        events = []
        while self._encoder.has_turn():
            events.append(self._TURN_TO_EVENT[self._encoder.read_turn()])
        if self._encoder.was_pressed():
            events.append(Input.PRESS)
        return events

    def _switch_to(self, screen_id):
        if self._current is not None:
            self._current.exit()
        self._current = self._screens[screen_id]
        self._current.enter()
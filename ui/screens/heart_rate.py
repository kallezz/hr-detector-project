from analysis.measuring import PpgSampler, update_bpm
from analysis.threshold import PeakDetector
from config import Display, Input, ScreenId
from hardware.ppg_sensor import PPGSensor
from ui.screen import Screen


class HeartRateScreen(Screen):
    """Shows the live BPM. Press to return to the menu."""

    def __init__(self, sampler=None, detector=None):
        self._sampler = sampler if sampler is not None else PpgSampler(PPGSensor())
        self._detector = detector if detector is not None else PeakDetector()
        self._bpm = None

    def enter(self):
        self._bpm = None
        self._detector.reset()
        self._sampler.start()

    def exit(self):
        self._sampler.stop()

    def handle_input(self, event):
        if event == Input.PRESS:
            return ScreenId.MENU
        return None

    def update(self):
        self._bpm = update_bpm(self._sampler, self._detector)
        return None

    def draw(self, display):
        display.clear()
        display.text("Heart rate", 0, 0)
        if self._bpm is None:
            display.text("BPM: --", 0, 3 * Display.LINE_HEIGHT)
        else:
            display.text("BPM: {}".format(self._bpm), 0, 3 * Display.LINE_HEIGHT)
        display.show()

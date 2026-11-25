from analysis.measuring import PpgSampler, update_bpm
from analysis.threshold import PeakDetector
from config import Display, Input, Pins, ScreenId, Ui
from hardware.ppg_sensor import PPGSensor
from led import Led
from ui.assets.measure_view import draw_measure_view
from ui.screen import Screen


class HeartRateScreen(Screen):


    def __init__(self):
        self._sampler = None
        self._detector = None
        self._led = None
        self._bpm = None
        self._beats = 0

    def enter(self):
        self._sampler = PpgSampler(PPGSensor())
        self._detector = PeakDetector()
        self._led = Led(Pins.HEARTBEAT_LED)
        self._bpm = None
        self._beats = 0
        self._sampler.start()

    def exit(self):
        self._sampler.stop()
        self._led.off()

    def handle_input(self, event):
        if event == Input.PRESS:
            return ScreenId.MENU
        return None

    def update(self):
        self._bpm = update_bpm(self._sampler, self._detector)
        beats = self._detector.get_beat_count()
        if beats != self._beats:
            self._beats = beats
            self._led.toggle()
        return None

    def draw(self, display):
        display.clear()
        points = self._detector.get_graph_points(Display.WIDTH)
        draw_measure_view(display, "Heart rate", self._bpm, "Press to go back", points)
        display.show()

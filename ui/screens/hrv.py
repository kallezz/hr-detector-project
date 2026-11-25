from analysis.hrv import HrvAnalysis
from analysis.measuring import PpgSampler, update_bpm
from analysis.ppi_recorder import PpiRecorder
from analysis.threshold import PeakDetector
from config import Analysis, Display, Input, Pins, ScreenId, Ui
from hardware.ppg_sensor import PPGSensor
from led import Led
from ui.assets.measure_view import draw_measure_view
from ui.screen import Screen
import time


class HrvScreen(Screen):
    

    def __init__(self):
        self._sampler = None
        self._detector = None
        self._recorder = None
        self._led = None
        self._bpm = None
        self._beats = 0
        self._result = None

    def enter(self):
        self._sampler = PpgSampler(PPGSensor())
        self._detector = PeakDetector()
        self._recorder = PpiRecorder()
        self._led = Led(Pins.HEARTBEAT_LED)
        self._bpm = None
        self._beats = 0
        self._result = None
        self._sampler.start()
        self._start_ms = time.ticks_ms()

    def exit(self):
        self._sampler.stop()
        self._led.off()

    def handle_input(self, event):
        if event == Input.PRESS:
            return ScreenId.MENU
        return None

    def update(self):
        if self._result is not None:
            return None
        self._bpm = update_bpm(self._sampler, self._detector)
        beats = self._detector.get_beat_count()
        if beats != self._beats:
            self._beats = beats
            self._led.toggle()
            self._recorder.add(self._detector.get_last_ppi_ms())
        elapsed_s = time.ticks_diff(time.ticks_ms(), self._start_ms) // 1000
        if self._recorder.is_done() or (
            elapsed_s >= Analysis.HRV_WINDOW_S + 1 and len(self._recorder.get_ppis()) >= 2
        ):
            self._finish()
        return None

    def draw(self, display):
        display.clear()
        if self._result is None:
            self._draw_measuring(display)
        else:
            self._draw_result(display)
        display.show()

    def _finish(self):
        self._sampler.stop()
        self._led.off()
        self._result = HrvAnalysis(self._recorder.get_ppis())

    def _draw_measuring(self, display):
        recorded_s = sum(self._recorder.get_ppis()) // 1000
        elapsed_s = time.ticks_diff(time.ticks_ms(), self._start_ms) // 1000
        seconds = min(Analysis.HRV_WINDOW_S, max(recorded_s, elapsed_s))
        footer = "{} / {} s".format(seconds, Analysis.HRV_WINDOW_S)
        points = self._detector.get_graph_points(Display.WIDTH)
        draw_measure_view(display, "HRV analysis", self._bpm, footer, points)
        
        
    def _draw_result(self, display):
        result = self._result
        display.text("HRV analysis", 0, 0)
        display.text("Mean PPI: {:.0f}".format(result.mean_ppi), 0, 2 * Display.LINE_HEIGHT)
        display.text("Mean HR: {:.0f}".format(result.mean_hr), 0, 3 * Display.LINE_HEIGHT)
        display.text("RMSSD: {:.0f}".format(result.rmssd), 0, 4 * Display.LINE_HEIGHT)
        display.text("SDNN: {:.0f}".format(result.sdnn), 0, 5 * Display.LINE_HEIGHT)
        display.text("Press to go back", 0, Display.HEIGHT - Display.LINE_HEIGHT)

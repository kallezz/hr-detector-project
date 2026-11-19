from machine import ADC, Pin
from fifo import Fifo
from piotimer import Piotimer
from config import Pins, Sampling
from hardware.ppg_sensor import PPGSensor


class PpgSampler:
    
    def __init__(self, sensor):
        self._sensor = PPGSensor()
        self._fifo = Fifo(Sampling.FIFO_SIZE)
        self._timer = None
        self._tick_handler = self._on_tick
        
        
    def start(self):
        
        self.stop()
        while self._fifo.has_data():
            self._fifo.get()
        self._timer = Piotimer(mode=Piotimer.PERIODIC, freq=Sampling.RATE_HZ,
                               callback=self._tick_handler)


    def stop(self):
        if self._timer is not None:
            self._timer.deinit()
            self._timer = None


    def read_new_samples(self):
        samples = []
        while self._fifo.has_data():
            samples.append(self._fifo.get())
        return samples


    def _on_tick(self, _state_machine):
        fifo = self._fifo
        if (fifo.head + 1) % fifo.size != fifo.tail:
            fifo.put(self._sensor.read())



if __name__ == "__main__":
    from analysis.threshold import PeakDetector
    from config import Ui
    

    sampler = PpgSampler(PPGSensor())
    detector = PeakDetector()
    sampler.start()
    while True:
        for sample in sampler.read_new_samples():
            if detector.update(sample):
                print("Heartbeat, BPM:", detector.get_bpm())
        

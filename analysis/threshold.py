from config import Analysis, Sampling

class PeakDetector:
    
    def __init__(self):
        self._window_size = Sampling.RATE_HZ * Analysis.THRESHOLD_WINDOW_S
        self._samples_per_minute = Sampling.RATE_HZ * 60
        self._min_interval = Analysis.MIN_PEAK_DISTANCE_MS * Sampling.RATE_HZ // 1000
        self._max_interval = self._samples_per_minute // Analysis.MIN_PLAUSIBLE_BPM
        self.reset()
    
    
    def reset(self):
        self._window = None
        self._write_pos = 0
        self._since_update = 0
        self._threshold = 0
        self._amplitude = 0
        self._previous = None
        self._sample_index = 0
        self._last_beat_index = None
        self._intervals = []
        self._last_ppi = None
        
        
    def get_bpm(self):
        if not self._intervals:
            return None
        mean_interval = sum(self._intervals) / len(self._intervals)
        return self._samples_per_minute / mean_interval
    
    
    def update(self, sample):
        if self._window is None:
            self._window = [sample] * self._window_size
        self._store_sample(sample)
        beat = self._is_beat(sample)
        self._previous = sample
        self._sample_index += 1
        if beat:
            self._register_beat()
        return beat
    
    
    def _store_sample(self, sample):
        self._window[self._write_pos] = sample
        self._write_pos = (self._write_pos + 1) % self._window_size
        self._since_update += 1
        if self._since_update >= Analysis.THRESHOLD_UPDATE_SAMPLES:
            self._since_update = 0
            self._update_threshold()
            
    
    def _update_threshold(self):
        low = min(self._window)
        high = max(self._window)
        self._amplitude = high - low
        self._threshold = low + int(self._amplitude * Analysis.PEAK_THRESHOLD_RATIO)

    def _is_beat(self, sample):
        if self._previous is None or self._amplitude < Analysis.MIN_SIGNAL_AMPLITUDE:
            return False
        crossed_up = self._previous < self._threshold <= sample
        return crossed_up and self._far_from_last_beat()

    def _far_from_last_beat(self):
        if self._last_beat_index is None:
            return True
        return (self._sample_index - self._last_beat_index) >= self._min_interval

    def _register_beat(self):
        if self._last_beat_index is not None:
            self._last_ppi = self._sample_index - self._last_beat_index
            self._add_interval(self._last_ppi)
        self._last_beat_index = self._sample_index
        
        
    def get_last_ppi_ms(self):
        if self._last_ppi is None:
            return None
        return self._last_ppi * 1000 // Sampling.RATE_HZ
    
        
    def _add_interval(self, interval):
        if interval > self._max_interval:
            self._intervals = []
            return
        self._intervals.append(interval)
        if len(self._intervals) > Analysis.BEATS_TO_AVERAGE:
            self._intervals.pop(0)

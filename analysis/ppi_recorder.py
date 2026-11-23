from config import Analysis


class PpiRecorder:
    

    def __init__(self):
        self._min_ppi = 60000 // Analysis.MAX_PLAUSIBLE_BPM
        self._max_ppi = 60000 // Analysis.MIN_PLAUSIBLE_BPM
        self.reset()

    def reset(self):
        self._ppis = []
        self._total_ms = 0
        self._previous = None

    def add(self, ppi):
    
        if ppi is None:
            return
        previous = self._previous
        self._previous = ppi
        if self._is_valid(ppi, previous):
            self._ppis.append(ppi)
            self._total_ms += ppi

    def is_done(self):
        return self._total_ms >= Analysis.HRV_WINDOW_S * 1000

    def get_ppis(self):
        return self._ppis

    def _is_valid(self, ppi, previous):
        if ppi < self._min_ppi or ppi > self._max_ppi:
            return False
        if previous is None:
            return True
        return abs(ppi - previous) <= previous * Analysis.MAX_PPI_CHANGE_RATIO
from math import sqrt


class HrvAnalysis:
    

    def __init__(self, ppis):
        self.mean_ppi = sum(ppis) / len(ppis)
        self.mean_hr = 60000 / self.mean_ppi
        self.sdnn = self._calculate_sdnn(ppis, self.mean_ppi)
        self.rmssd = self._calculate_rmssd(ppis)

    def _calculate_sdnn(self, ppis, mean_ppi):
        squares = [(ppi - mean_ppi) ** 2 for ppi in ppis]
        return sqrt(sum(squares) / (len(ppis) - 1))

    def _calculate_rmssd(self, ppis):
        squares = [(ppis[i + 1] - ppis[i]) ** 2 for i in range(len(ppis) - 1)]
        return sqrt(sum(squares) / len(squares))
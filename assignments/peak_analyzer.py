from filefifo import Filefifo


class PeakFrequencyAnalyzer:
    FILE_NAMES = [
        "sinewave_250Hz_01.txt",
        "sinewave_250Hz_02.txt",
        "sinewave_250Hz_03.txt",
    ]

    def __init__(self, sample_rate=250, target_intervals=3, samples_to_skip=500):
        self.sample_rate = sample_rate
        self.target_intervals = target_intervals
        self.samples_to_skip = samples_to_skip
        self._reset(start_index=samples_to_skip)

    def _reset(self, start_index=0):
        # peak detection state
        self.prev_sample = None
        self.rising = False

        # frequency counting state
        self.sample_index = start_index   # index of the most recent sample
        self.last_peak = None
        self.intervals = []               # list of (samples, seconds)
        self.finished = False

    def update(self, sample):
        """Feed one sample. Returns True once enough intervals are collected."""
        if self.finished:
            return True

        self.sample_index += 1

        if self.prev_sample is not None:
            is_rising = sample > self.prev_sample
            is_diving = sample < self.prev_sample

            # was rising, now falling -> previous sample was the peak
            if self.rising and is_diving:
                self._register_peak(self.sample_index - 1)

            if is_rising:
                self.rising = True
            elif is_diving:
                self.rising = False

        self.prev_sample = sample
        return self.finished

    def _register_peak(self, peak_index):
        if self.last_peak is not None:
            sample_diff = peak_index - self.last_peak
            self.intervals.append((sample_diff, sample_diff / self.sample_rate))

            if len(self.intervals) >= self.target_intervals:
                self.finished = True

        self.last_peak = peak_index

    def print_results(self):
        if not self.intervals:
            print("Not enough peaks detected.")
            return

        for number, (samples, seconds) in enumerate(self.intervals, start=1):
            print(f"{number}) int: {samples}-{int(seconds * 1000)}ms")

        avg_samples = sum(s for s, _ in self.intervals) / len(self.intervals)
        frequency = self.sample_rate / avg_samples
        print(f"Frequency: {frequency:.4f} Hz\n")

    def run(self):
        """Ask which file to analyze, process it, and print the results."""
        print("Select file 0,1 or 2:")
        file_num = int(input())

        data = Filefifo(10, name=self.FILE_NAMES[file_num])

        # start from a clean state so run() can be called more than once
        self._reset(start_index=self.samples_to_skip)

        for _ in range(self.samples_to_skip):
            data.get()

        while data.has_data():
            if self.update(data.get()):
                break

        self.print_results()


if __name__ == "__main__":
    analyzer = PeakFrequencyAnalyzer()
    analyzer.run()

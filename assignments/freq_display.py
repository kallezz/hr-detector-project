from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


class FrequencyDisplay:
    FILE_NAMES = [
        "/data/sinewave_250Hz_01.txt",
        "/data/sinewave_250Hz_02.txt",
        "/data/sinewave_250Hz_03.txt",
    ]
    SF = 250
    SAMPLES_TO_READ = 500  # 2 seconds for calibration
    FONT_SIZE = 8
    MAX_LINES = 8

    def __init__(self, file_num):
        i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled = SSD1306_I2C(128, 64, i2c)
        if 0 <= file_num < len(self.FILE_NAMES):
            self.file_name = self.FILE_NAMES[file_num]
        else:
            self.file_name = self.FILE_NAMES[0]
        self.threshold = 0

    def _measure(self):
        data = Filefifo(10, name=self.file_name)

        # 1. Read two seconds of data and find min/max
        calibration = []
        while len(calibration) < self.SAMPLES_TO_READ and data.has_data():
            calibration.append(data.get())

        if not calibration:
            return 0, []

        self.threshold = (min(calibration) + max(calibration)) / 2

        # 2. Find rising edges (below threshold -> at/above threshold)
        crossing_indices = []
        prev_sample = None
        index = 0

        for sample in calibration:
            if prev_sample is not None and prev_sample < self.threshold <= sample:
                crossing_indices.append(index)
            prev_sample = sample
            index += 1

        while data.has_data():
            sample = data.get()
            if prev_sample is not None and prev_sample < self.threshold <= sample:
                crossing_indices.append(index)
            prev_sample = sample
            index += 1

        # 3. Intervals between consecutive rising edges
        results = []
        for j in range(len(crossing_indices) - 1):
            diff_samples = crossing_indices[j + 1] - crossing_indices[j]
            diff_seconds = diff_samples / self.SF
            results.append({"samples": diff_samples, "seconds": round(diff_seconds, 3)})

        frequency = 0
        if results:
            avg_samples = sum(r["samples"] for r in results) / len(results)
            frequency = self.SF / avg_samples

        return frequency, results

    def _show_results(self, frequency, results):
        self.oled.fill(0)
        line = 0
        font_size = self.FONT_SIZE

        # Leave the last line free for the frequency
        for result in results[:self.MAX_LINES - 1]:
            self.oled.text(f"{result['samples']} - {result['seconds']}s", 0, line * font_size)
            line += 1

        self.oled.text(f"f={frequency:.2f}Hz", 0, (self.MAX_LINES - 1) * font_size)
        self.oled.show()

    def run(self):
        frequency, results = self._measure()
        for result in results:
            print(f"{result['samples']} - {result['seconds']}s")
        print(f"Calculated frequency: {frequency:.4f} Hz")
        self._show_results(frequency, results)


if __name__ == "__main__":
    print("Select file 0, 1 or 2:")
    try:
        file_num = int(input())
    except ValueError:
        file_num = 0
    FrequencyDisplay(file_num).run()
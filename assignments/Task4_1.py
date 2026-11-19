from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


class SlopeInspection:
    SAMPLING_RATE = 250
    FILE_PATH = "/data/hr_capture02_250Hz.txt"
    SF = 250
    CALIBRATION_SAMPLES = 500   
    MEASURE_SAMPLES = 8000
    
    
    def __init__(self):
        i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled = SSD1306_I2C(128, 64, i2c)
        self.fifo = Filefifo(10, name=self.FILE_PATH)
        
    
    def _measure(self):
        data = Filefifo(10, name=self.FILE_PATH)

        
        min_val = max_val = None
        for _ in range(self.CALIBRATION_SAMPLES):
            s = data.get()
            if min_val is None or s < min_val:
                min_val = s
            if max_val is None or s > max_val:
                max_val = s
        self.threshold = min_val + (max_val-min_val) * 100 // 100

        
        crossings = []
        prev = None
        min_peak_distance = 100
        
        for i in range(self.MEASURE_SAMPLES):
            s = data.get()
            if prev is not None and prev < self.threshold <= s:
                if not crossings or (i - crossings[-1]) > min_peak_distance:    
                    crossings.append(i)
            prev = s

        
        results = []
        for j in range(len(crossings) - 1):
            samples = crossings[j + 1] - crossings[j]
            results.append({"samples": samples,
                            "HR_BPM": 60 * self.SF / samples})

        bpm = 0
        if results:
            avg = sum(r["samples"] for r in results) / len(results) / self.SF
            bpm = (1.0 / avg) * 60 if avg > 0 else 0
        return bpm, results


    def run(self):
        bpm, results = self._measure()
        
        for item in results[:20]:
            print("Heart rate: {:.0f}bpm".format(item["HR_BPM"]))
            
        
        self.oled.fill(0)
        for i, res in enumerate(results[:5]):
            self.oled.text("Heartrate: {:.0f}bpm".format(res["HR_BPM"]), 0, i * 8, 1)
            

        self.oled.text("Avg: {:.0f}bpm".format(bpm), 0, 56, 1)
        self.oled.show()


if __name__ == "__main__":
    SlopeInspection().run()

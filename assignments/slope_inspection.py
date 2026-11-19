from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


class SlopeInspection:
    SAMPLING_RATE = 250
    FILE_PATH = "/data/sinewave_250Hz_01.txt"
    
    def __init__(self):
        i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled = SSD1306_I2C(128, 64, i2c)
        self.fifo = Filefifo(10, name=self.FILE_PATH)
    
    def run(self):
        samples = []
        
        for _ in range(1000):
            if self.fifo.has_data():
                samples.append(self.fifo.get())
        
        peak_indices = []
        
        for i in range(1, len(samples) - 1):
            prev_slope = samples[i] - samples[i - 1]
            next_slope = samples[i + 1] - samples[i]
            
            if prev_slope > 0 and next_slope <= 0:
                peak_indices.append(i)

        print(f"Total peaks found: {len(peak_indices)}")
        
        if len(peak_indices) >= 4:
            print("\n--- Peak-to-Peak Intervals ---")
            intervals_samples = []
            intervals_seconds = []
            results = []
            
            for j in range(3):
                p1 = peak_indices[j]
                p2 = peak_indices[j + 1]
                diff_samples = p2 - p1
                diff_seconds = diff_samples / self.SAMPLING_RATE
                
                intervals_samples.append(diff_samples)
                intervals_seconds.append(diff_seconds)
                
                results.append({"samples": diff_samples, "seconds": diff_seconds})
                
                print(f"Interval {j+1}: {diff_samples} samples, {diff_seconds:.4f} seconds")
            
            avg_interval_sec = sum(intervals_seconds) / len(intervals_seconds)
            frequency = 1.0 / avg_interval_sec
            
            print(f"\nCalculated Signal Frequency: {frequency:.2f} Hz")
            
            self.oled.fill(0)
            self.oled.text(f"Freq: {frequency:.1f} Hz", 0, 0)
            
            font_size = 8
            line = 1
            
            for result in results:
                self.oled.text(f"{result["samples"]} - {result["seconds"]}s", 0, line * font_size)
                line += 1
            
            self.oled.show()
        else:
            print("Not enough peaks found to calculate 3 intervals.")
            self.oled.fill(0)
            self.oled.text("Peak error", 0, 0)
            self.oled.show()

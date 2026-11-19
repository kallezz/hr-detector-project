from machine import ADC, Pin
from config import Pins


class PPGSensor:
    def __init__(self, pin=Pins.PPG_SENSOR_ADC):
        self._adc = ADC(Pin(pin))
    
    def read(self):
        return self._adc.read_u16()

if __name__ == "__main__":
    while True:
        print(PPGSensor().read())

import time
from machine import Pin


class Led:
    

    def __init__(self, pin):
        self._pin = Pin(pin, Pin.OUT)
        self._pulse_end_ms = None
        self.off()


    def on(self):
        self._pin.value(1)


    def off(self):
        self._pulse_end_ms = None
        self._pin.value(0)


    def pulse(self, duration_ms=100):
        self._pulse_end_ms = time.ticks_add(time.ticks_ms(), duration_ms)
        self.on()


    def update(self):
        if self._pulse_end_ms is not None:
            if time.ticks_diff(self._pulse_end_ms, time.ticks_ms()) <= 0:
                self.off()
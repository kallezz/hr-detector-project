from time import ticks_ms, ticks_diff
from machine import Pin
from fifo import Fifo
from config import Pins, Encoder as EncoderConfig


class Encoder:
    """The IRQs only queue turn events and set a press flag; the main loop reads them."""

    def __init__(self, pin_a=Pins.ENCODER_A, pin_b=Pins.ENCODER_B,
                 pin_button=Pins.ENCODER_BUTTON):
        self._pin_a = Pin(pin_a, mode=Pin.IN)
        self._pin_b = Pin(pin_b, mode=Pin.IN)
        self._pin_button = Pin(pin_button, mode=Pin.IN, pull=Pin.PULL_UP)
        self._events = Fifo(EncoderConfig.FIFO_SIZE, typecode=EncoderConfig.FIFO_TYPECODE)
        self._pressed = False
        self._last_press_ms = ticks_ms()
        self._pin_a.irq(handler=self._on_turn, trigger=Pin.IRQ_RISING, hard=True)
        self._pin_button.irq(handler=self._on_press, trigger=Pin.IRQ_FALLING, hard=True)

    def _on_turn(self, pin):
        """IRQ handler: queue the direction only, no drawing or waiting."""
        if self._pin_b():
            self._events.put(EncoderConfig.TURN_LEFT)
        else:
            self._events.put(EncoderConfig.TURN_RIGHT)

    def _on_press(self, pin):
        """IRQ handler: debounce and set the flag, nothing else."""
        now = ticks_ms()
        if ticks_diff(now, self._last_press_ms) > EncoderConfig.BUTTON_DEBOUNCE_MS:
            self._pressed = True
            self._last_press_ms = now

    def has_turn(self):
        return self._events.has_data()

    def read_turn(self):
        """Return TURN_LEFT or TURN_RIGHT from the queue."""
        return self._events.get()

    def was_pressed(self):
        """Return True once per press, then clear the flag."""
        if self._pressed:
            self._pressed = False
            return True
        return False


if __name__ == "__main__":
    # Debug only: turn and press the encoder and watch the console
    encoder = Encoder()
    while True:
        if encoder.has_turn():
            print("turn", encoder.read_turn())
        if encoder.was_pressed():
            print("press")
from machine import Pin


class Button:
    def __init__(self, pin):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
    
    def pressed(self):
        if self.button.value() == 0:
            return True
        
        return False

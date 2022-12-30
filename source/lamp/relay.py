import time
from machine import Pin


class Relay:
    # PIN21
    def __init__(self, relay_pin):
        self._pin = Pin(relay_pin, Pin.OUT)

    def status(self):
        return self._pin.value()

    def switch_on(self):
        self._pin.high()

    def switch_off(self):
        self._pin.low()

    def toggle(self):
        self._pin.toggle()




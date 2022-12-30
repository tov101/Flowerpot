from machine import Pin, PWM


class WaterPump:
    ON = True
    OFF = False

    def __init__(self, pin):
        self._pin = Pin(pin, Pin.OUT, value=0)

    def status(self):
        return bool(self._pin.value())

    def switch_on(self):
        self._pin.high()

    def switch_off(self):
        self._pin.low()

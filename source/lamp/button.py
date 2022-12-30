from machine import Pin


class Button:
    def __init__(self, input_pin, handler):
        self._pin = Pin(input_pin, Pin.IN, Pin.PULL_UP)
        self._pin.irq(lambda pin: handler(), Pin.IRQ_FALLING)


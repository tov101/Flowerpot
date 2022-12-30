from machine import Pin
from .dht11 import DHT11


class Environment:

    def __init__(self, pin):
        self._dht = DHT11(Pin(pin, Pin.IN))

    def temperature(self):
        self._dht.measure()
        return self._dht.temperature

    def humidity(self):
        self._dht.measure()
        return self._dht.humidity

    def measure(self):
        self._dht.measure()
        return self._dht.temperature, self._dht.humidity

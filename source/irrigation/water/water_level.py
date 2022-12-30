from machine import ADC


class WaterLevel:
    # V: Percent
    # 0.0V: 0%
    # 2.6: 100%
    MIN_V = 0.03
    MAX_V = 2.6

    EMPTY = True

    def __init__(self, pin, vref):
        self._vref = vref
        self._adc = ADC(pin)
        self._conversion_factor = vref / (65535)

    def raw(self):
        return self._adc.read_u16()

    def measure(self):
        # Because of shitty sensor, consider that less than 1.5V means empty tank
        vin = self.raw() * self._conversion_factor
        return vin < 1.5
        # percentage = (vin * 100) / WaterLevel.MAX_V

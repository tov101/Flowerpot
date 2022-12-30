from machine import ADC


class SoilHumidity:
    # V: Percent
    # 0.75: 100%
    # 4.37: 0%
    MIN_V = 0.75
    MAX_V = 4.37

    def __init__(self, pin, vref):
        self._vref = vref
        self._adc = ADC(pin)
        self._conversion_factor = vref / (65535)

    def raw(self):
        return self._adc.read_u16()

    def measure(self):
        vin = self.raw() * self._conversion_factor
        if vin < SoilHumidity.MIN_V:
            return 100
        if vin > SoilHumidity.MAX_V:
            return 0

        percentage = 100 - (vin * 100) / SoilHumidity.MAX_V
        return percentage

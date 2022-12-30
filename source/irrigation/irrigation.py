import time

from .soil import SoilHumidity
from .water.water_level import WaterLevel
from .water.water_pump import WaterPump

VREF = 5

class Irrigation:
    # Irrigation Time 10s
    IRRIGATION_TIME = 10

    def __init__(self, water_read_pin, water_write_pin, *soil_sensor_pin):
        self._water_level = WaterLevel(water_read_pin, VREF)
        self._water_pump = WaterPump(water_write_pin)

        self._soil_sensors = [SoilHumidity(pin, VREF) for pin in soil_sensor_pin]

    def water_level(self):
        return self._water_level.measure()

    def water_pump(self):
        return self._water_pump.status()

    def set_water_pump(self, state):
        if state:
            self._water_pump.switch_on()
        else:
            self._water_pump.switch_off()

    def soil_humidity(self, soil_sensor=None):
        if soil_sensor:
            return soil_sensor.measure()

        average = 0
        for s in self._soil_sensors:
            average += s.measure()
        return average / len(self._soil_sensors)

    def need_irrigation(self):
        # If Humidity is less than 10%
        return self.soil_humidity() < 10

    def irrigate(self):
        # If Tank is empty, do not irrigate
        if self.water_level() == WaterLevel.EMPTY:
            return
        timeout = Irrigation.IRRIGATION_TIME
        # Periodically read WaterLevel
        try:
            # TODO: Avoid while here if you're gonna call this via Timer Interrupt
            while self.need_irrigation() and timeout > 0 and self.water_level() != WaterLevel.EMPTY:
                if self.water_pump() == WaterPump.OFF:
                    self.set_water_pump(state=WaterPump.ON)
                time.sleep(0.1)
                timeout -= 0.1
        except Exception as error:
            pass
        finally:
            # Set Pump Off
            self.set_water_pump(state=WaterPump.OFF)



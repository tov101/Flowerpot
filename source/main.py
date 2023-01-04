import sys
import time
from machine import Pin
from _thread import start_new_thread

from globals import (
    PIN_BUTTON,
    PIN_DHT,
    PIN_RELAY,
    PIN_SOIL_SENSOR_0,
    PIN_SOIL_SENSOR_1,
    PIN_WATER_LEVEL_SENSOR,
    PIN_WATER_PUMP
)
from environment.environment import Environment
from irrigation.irrigation import Irrigation
from lamp.uvlamp import UVLamp
from mini_os import add_task, start

# Init WiFi

# Init Env
env = Environment(PIN_DHT)

# Init Photoresist

# Init Irrigation (water_read_pin, water_write_pin, *soil_sensors)
irrigation = Irrigation(
    PIN_WATER_LEVEL_SENSOR,
    PIN_WATER_PUMP,
    PIN_SOIL_SENSOR_0,
    PIN_SOIL_SENSOR_1
)
# Init UVLamp (button_pin, relay_pin, cycle_time)
uvlamp = UVLamp(PIN_BUTTON, PIN_RELAY)


# Define Monitoring Task
def monitor(period):
    while True:
        data = {}
        try:
            t, h = env.measure()
            data["EnvironmentTemperature"] = t
            data["EnvironmentHumidity"] = t
        except:
            pass
        data['UVLamp State'] = uvlamp.status()
        data['WaterLevel Empty'] = irrigation.water_level()
        data['WaterPump State'] = irrigation.water_pump()
        data['SoilHumidity'] = irrigation.soil_humidity()
        # TODO: Send over nRF
        time.sleep(period)
        print(data)


# Set UVLamp Cycle to 12h
add_task(uvlamp.toggle, 12 * 60 * 60)
# Set Irrigation Cycle to 24h
# Scheduler.add_task(Task(24 * 60 * 60, irrigation.irrigate))
add_task(irrigation.irrigate, 15)

# Launch 2nd Task
start_new_thread(monitor, (1,))

# Run Scheduler
start()


import time
import RPi.GPIO as GPIO
from controller import Relay, Sensor

sensor_data = Sensor(22)
pump = Relay(23)
sensor = Relay(24)


def init():
    print("-- START --")
    sensor_data.init("Sensor output data")
    pump.init("Pump Relay")
    sensor.init("Sensor Relay")
    print("-- START --\n")


def now():
    return time.strftime("%d/%m/%y - %H:%M", time.localtime())


def sensor_output():
    sensor.on()
    time.sleep(2)
    reading = sensor_data.output()
    timestemp = now()
    time.sleep(1)
    sensor.off()
    print(timestemp, "- sensor output:", ("dry" if reading else "wet"))
    return reading, timestemp


try:
    init()
    sensor_output()

finally:
    print("\n-- END -- \ncleaning GPIO channels...")
    GPIO.cleanup()

import RPi.GPIO as GPIO
from controller import Relay, Sensor
import time

data = Sensor(22)
pump = Relay(23)
sensor = Relay(24)


def init():
    print("-- START --")
    data.init("Sensor output")
    pump.init("Pump")
    sensor.init("Sensor")


def now():
    return time.strftime("%d/%m/%y - %H:%M", time.localtime())


def sensor_output():
    sensor.on()
    time.sleep(2)
    sensor_data = "dry" if data.output() else "wet"
    time.sleep(1)
    sensor.off()
    print(now(), "- sensor output:", sensor_data)
    return sensor_data


try:
    init()
    sensor_output()

finally:
    print("-- END -- cleaning GPIO channels...")
    GPIO.cleanup()

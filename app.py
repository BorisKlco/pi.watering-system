import time
import RPi.GPIO as GPIO
from controller import Relay, Sensor

sensor_data = Sensor(22)
pump = Relay(23)
sensor = Relay(24)
last_watering = time.time()


def init():
    print("-- START --")
    sensor_data.init("Sensor output data")
    pump.init("Pump Relay")
    sensor.init("Sensor Relay")
    print("-- START --\n")


def now():
    return time.strftime("%d/%m/%y - %H:%M:%S", time.localtime())


def sensor_output():
    timestemp = now()
    sensor.on()
    time.sleep(2)
    reading = sensor_data.output()
    time.sleep(1)
    sensor.off()
    print(timestemp, "- sensor output:", ("dry" if reading else "wet"))
    return reading


def water(sec=5):
    # ~10ml = 1sec
    print(f"{now()} - Watering for {sec}s...")
    pump.on()
    time.sleep(sec)
    pump.off()
    print(f"{now()} - Watering done...")


try:
    init()

    while True:
        time.sleep(1)
        print(time.time() - last_watering)

finally:
    print("\n-- END -- \ncleaning GPIO channels...")
    GPIO.cleanup()

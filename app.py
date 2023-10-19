import os
import time
import math
import requests
import RPi.GPIO as GPIO
from picamera import PiCamera
from controller import Relay, Sensor


sensor_data = Sensor(22)
pump = Relay(23)
sensor = Relay(24)
camera = PiCamera()
camera.resolution = (1280, 720)

last_watering = time.time()
SLEEP_INTERVAL = 1  # 8 hour - 28800
WATERING_INTERVAL = 6  # 24 hour - 86400
SERVER = "http://127.0.0.1:5173/store-record"


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


def record():
    try:
        camera.start_preview()
        photo_name = time.strftime("%y%m%d%H") + ".jpg"
        data_photo = os.getcwd() + "/photos/" + photo_name
        time.sleep(2)
        camera.capture(data_photo)

        data = {"filename": photo_name}

        files = {"file": (photo_name, open(data_photo, "rb"))}
        req = requests.post(SERVER, data=data, files=files, timeout=15)
        print("Sending record -> ", req.text, req.status_code)
    except:
        print("Error while sending record...")


try:
    init()

    while True:
        time.sleep(SLEEP_INTERVAL)
        watering_diff = math.floor(time.time() - last_watering)
        water_now = True if watering_diff > WATERING_INTERVAL else False
        dry_soil = sensor_output()
        print("INFO: ", last_watering, water_now)
        if dry_soil and water_now:
            print("WATERING!!!")
            # water()
            # record()
            last_watering = time.time()

finally:
    print("\n-- END -- \ncleaning GPIO channels...")
    GPIO.cleanup()

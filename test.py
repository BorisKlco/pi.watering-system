import time
import os
import math
import requests

last_watering = time.time()
SLEEP_INTERVAL = 1  # 1 hour - 3600
WATERING_INTERVAL = 6  # 12 hour - 43200
SERVER = "http://127.0.0.1:5173/"


def record(photo_name):
    try:
        data_time = time.time()
        data_photo = os.getcwd() + "/" + photo_name
        photo_name = time.strftime("%y%m%d%H") + ".jpg"

        data = {"time": data_time, "filename": photo_name}

        files = {"file": (photo_name, open(data_photo, "rb"))}
        print(data, files)
        req = requests.post(SERVER, data=data, files=files, timeout=15)
        print("Sending record -> ", req.text, req.status_code)
    except:
        print("Error while sending record...")


record("cat.jpg")

# while True:
#     time.sleep(SLEEP_INTERVAL)
#     watering_diff = math.floor(time.time() - last_watering)
#     water_now = True if watering_diff > WATERING_INTERVAL else False
#     dry_soil = False  # sensor_output()
#     print("INFO: ", last_watering, water_now)
#     if dry_soil or water_now:
#         print("WATERING!!!")
#         last_watering = time.time()

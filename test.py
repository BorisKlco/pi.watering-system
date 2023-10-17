import time
import os
import math
import requests

last_watering = time.time()
SLEEP_INTERVAL = 1  # 1 hour - 3600
WATERING_INTERVAL = 6  # 12 hour - 43200
SERVER = "http://127.0.0.1:5173/"


def record():
    try:
        data_time = time.time()
        data_snapshot = "path/to/file"
        snapshot_name = time.strftime("%y-%m-%d-%h") + ".jpg"

        data = {"time": data_time}

        files = {"file": (snapshot_name, open(data_snapshot, "rb"))}
        print(data, files)
        requests.post(SERVER, data=data, files=files, timeout=15)
        return "Record send..."
    except:
        return "Error while sending record..."


# while True:
#     time.sleep(SLEEP_INTERVAL)
#     watering_diff = math.floor(time.time() - last_watering)
#     water_now = True if watering_diff > WATERING_INTERVAL else False
#     dry_soil = False  # sensor_output()
#     print("INFO: ", last_watering, water_now)
#     if dry_soil or water_now:
#         print("WATERING!!!")
#         last_watering = time.time()

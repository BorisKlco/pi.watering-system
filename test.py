import time
import os
import math
import requests

last_watering = time.time()
SLEEP_INTERVAL = 1  # 1 hour - 3600
WATERING_INTERVAL = 6  # 12 hour - 43200
SERVER = "http://127.0.0.1:5173/"


data_text = "Hello"
data_snapshot = os.path.join(os.getcwd(), "cat.jpg")

data = {"text": data_text}

files = {"file": ("cat.jpg", open(data_snapshot, "rb"))}
print(data, files)
req = requests.post(SERVER, data=data, files=files)

# while True:
#     time.sleep(SLEEP_INTERVAL)
#     watering_diff = math.floor(time.time() - last_watering)
#     water_now = True if watering_diff > WATERING_INTERVAL else False
#     dry_soil = False  # sensor_output()
#     print("INFO: ", last_watering, water_now)
#     if dry_soil or water_now:
#         print("WATERING!!!")
#         last_watering = time.time()

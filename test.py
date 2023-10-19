import time
import os
import math
import requests

last_watering = time.time()
SLEEP_INTERVAL = 1  # 1 hour - 3600
WATERING_INTERVAL = 6  # 12 hour - 43200
SERVER = "http://127.0.0.1:5173/store-record"


def record(photo_name):
    try:
        data_photo = os.getcwd() + "/photos/" + photo_name
        photo_name = time.strftime("%y%m%d%H") + ".jpg"

        data = {"filename": photo_name}

        files = {"file": (photo_name, open(data_photo, "rb"))}
        req = requests.post(SERVER, data=data, files=files, timeout=15)
        print("Sending record -> ", req.text, req.status_code)
    except:
        print("Error while sending record...")


record("cat.jpg")

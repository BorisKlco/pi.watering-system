# crontab -e
# 0 8 * * * python3 record.py
# 0 12 * * * python3 record.py
# 0 19 * * * python3 record.py

import os
import time
import requests
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1280, 1024)

SERVER = "http://127.0.0.1:5173/store-record"

def record():
    try:
        camera.start_preview()
        camera.annotate_text = time.strftime("%d/%m/%y - %H:%M:%S")
        camera.annotate_text_size = 50
        photo_name = time.strftime("%y%m%d-%H-%M") + ".jpg"
        data_photo = os.getcwd() + "/photos/" + photo_name
        time.sleep(2)
        camera.capture(data_photo, quality=100)

        data = {"filename": photo_name, "water": 0}

        files = {"file": (photo_name, open(data_photo, "rb"))}
        req = requests.post(SERVER, data=data, files=files, timeout=15)
        print("Sending record -> ", req.text, req.status_code)
    except:
        print("Error while sending record...")


record()

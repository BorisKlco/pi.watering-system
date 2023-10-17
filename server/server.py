import os
import time
from flask import Flask, request

app = Flask(__name__)
SERVER_TYPE = "exposed"  # 'caddy, 'exposed'
WHITELIST = ["127.0.0.1"]
PHOTO_FOLDER = os.getcwd()


@app.route("/", methods=["POST"])
def index():
    try:
        if SERVER_TYPE == "caddy":
            # caddy reverse_proxy
            request_ip = request.headers["X-Forwarded-For"]
        else:
            request_ip = request.remote_addr

        if request_ip not in WHITELIST:
            print("IP not allowed...")
            return "IP not allowed...", 401

        photo = request.files.get("file")
        if request.form.get("filename") is None:
            photo_name = time.strftime("%y%m%d%H") + ".jpg"
        else:
            photo_name = request.form.get("filename")

        path_to_photo = os.path.join(PHOTO_FOLDER, photo_name)  # type: ignore

        watering_time = request.form.get("time")

        photo.save(path_to_photo)  # type: ignore

        # Save data to db
        print("Saving data...Brrrrr: ", watering_time, path_to_photo)
        ###

        return "Data accepted...", 200
    except:
        return "Error", 406


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5173)

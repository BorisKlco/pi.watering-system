import os
import time
from PIL import Image
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from moviepy.editor import ImageSequenceClip

SERVER_TYPE = "caddy"  # 'caddy, 'exposed'
WHITELIST = [""]
PHOTO_FOLDER = os.getcwd()
DB = "sqlite:///" + PHOTO_FOLDER + "/db.sqlite3"

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String)
    path = db.Column(db.String)
    image = db.Column(db.String)
    water = db.Column(db.Integer, default=50)

    def __repr__(self):
        return f"-\nID:{self.id}\nTIME:{self.time}\nPHOTO:{self.image}\nPATH:{self.path}\n-"


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def main_page():
    with open('/home/ubuntu/ip.txt', 'a') as file:
        file.write(request.headers["X-Forwarded-For"] + '\n')
    return render_template("index.html")


@app.route("/watering", methods=["GET"])
def last_watering():
    record = Records.query.order_by(Records.id.desc()).first()
    return render_template("watering.html", time=record.time, photo=record.image)


@app.route("/history", methods=["GET"])
def history():
    records = Records.query.order_by(Records.id.desc()).all()
    count = Records.query.count()
    return render_template("history.html", count=count, history=records)


@app.route("/store-record", methods=["POST"])
def index():
    try:
        ###### IP CHECK
        if SERVER_TYPE == "caddy":
            # caddy reverse_proxy
            request_ip = request.headers["X-Forwarded-For"]
        else:
            request_ip = request.remote_addr

        if request_ip not in WHITELIST:
            print("IP not allowed...")
            return "IP not allowed...", 401

        ###### TIME DATA
        watering_time = time.strftime("%d/%m/%y - %H:%M:%S")

        ###### PHOTO
        photo = request.files.get("file")
        if request.form.get("filename") is None:
            photo_name = time.strftime("%y%m%d-%H-%M") + ".jpg"
        else:
            photo_name = request.form.get("filename")

        path_to_photo = os.path.join(PHOTO_FOLDER, "static/images", photo_name)  # type: ignore
        photo.save(path_to_photo)  # type: ignore

        compr = Image.open(path_to_photo)
        compr.save(path_to_photo, quality=95)
        clip = ImageSequenceClip("static/images", fps=1)
        clip.write_videofile("static/video/video.mp4")

        ###### SAVE TO DB
        data_for_db = Records(time=watering_time, image=photo_name, path=path_to_photo)
        db.session.add(data_for_db)
        db.session.commit()
        ###### SAVE TO DB

        return "Data accepted...", 200
    except:
        return "Error", 406


if __name__ == "__main__":
    app.run(threaded=True, debug=False, port=3000)

import os
import time
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

SERVER_TYPE = "exposed"  # 'caddy, 'exposed'
WHITELIST = ["127.0.0.1"]
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
    image = db.Column(db.String)
    water = db.Column(db.Integer, default=50)

    def __repr__(self):
        return f"-\nID:{self.id}\nTIME:{self.time}\nPHOTO:{self.image}\n-"


with app.app_context():
    db.create_all()


@app.route("/q", methods=["GET"])
def get_records():
    records = Records.query.order_by(Records.id.desc()).all()
    count = Records.query.count()
    return render_template("index.html", records=records, count=count)


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
        watering_time = request.form.get("time")

        ###### PHOTO
        photo = request.files.get("file")
        if request.form.get("filename") is None:
            photo_name = time.strftime("%y%m%d%H") + ".jpg"
        else:
            photo_name = request.form.get("filename")

        path_to_photo = os.path.join(PHOTO_FOLDER, photo_name)  # type: ignore
        photo.save(path_to_photo)  # type: ignore

        ###### SAVE TO DB
        data_for_db = Records(time=watering_time, image=path_to_photo)
        db.session.add(data_for_db)
        db.session.commit()
        ###### SAVE TO DB

        return "Data accepted...", 200
    except:
        return "Error", 406


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5173)

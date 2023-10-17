import os
from flask import Flask, request

app = Flask(__name__)
SERVER_TYPE = "exposed"  # 'caddy, 'exposed'


@app.route("/", methods=["POST"])
def index():
    try:
        if SERVER_TYPE == "caddy":
            # caddy reverse_proxy
            request_ip = request.headers["X-Forwarded-For"]
        else:
            request_ip = request.remote_addr
        print(request_ip)

        snapshot = request.files.get("file")
        data_text = request.form.get("text")
        print("DATA", data_text)
        if snapshot:
            snapshot.save(os.path.join(os.getcwd(), "random.jpg"))
        return "Hi"
    except:
        return "Error"


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5173)

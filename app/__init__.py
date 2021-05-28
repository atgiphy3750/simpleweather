from datetime import datetime
import io
from flask.templating import render_template
from app.data.data import weather_data
from flask import Flask
import json
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    mimetypes.add_type("text/javascript", ".js")
    return render_template("index.html")


@app.route("/data", methods=["POST"])
def get_data():
    try:
        data = handle_json_success()
        print("try success")
    except:
        data = handle_json_failure()
        print("try failure")
    return data


def handle_json_success():
    saved_data = os.path.join(app.static_folder, "weather.json")  # type:ignore
    with open(saved_data, "r", encoding="utf-8") as saved:
        data = json.load(saved)
        create_time_str = data.get("0").get("createTime")
        create_time = datetime.strptime(create_time_str, r"%Y%m%d%H%M")
        hour_diff = sub_hour(create_time, datetime.now())
        if hour_diff > 3:
            raise Exception
        return data


def handle_json_failure():
    data = weather_data()
    saved_data = os.path.join(app.static_folder, "weather.json")  # type:ignore
    with open(saved_data, "w", encoding="utf-8") as saved:
        json.dump(data, saved)
        return data


def sub_hour(before: datetime, after: datetime):
    diff = after - before
    diff_second = diff.total_seconds()
    hours = divmod(diff_second, 3600)[0]
    return hours


import mimetypes

print(mimetypes.guess_type("index.js"))

from datetime import datetime
import io
from flask.templating import render_template
from app.data.data import data
from flask import Flask
import json
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/data", methods=["POST"])
def get_data():
    saved_json = os.path.join(app.static_folder, "weather.json")  # type:ignore
    with open(saved_json, encoding="utf-8") as saved:
        if os.path.exists(saved_json):
            try:
                data_ = json.load(saved)
                print("read")
            except io.UnsupportedOperation:
                data_ = data()
                json.dump(data_, saved)
                print("empty file")
                return data_
            create_time_str = data_.get("0").get("createTime")
            if create_time_str:
                create_time = datetime.strptime(create_time_str, r"%Y%m%d%H%M")
                hour_diff = sub_hour(create_time, datetime.now())
                if hour_diff < 3:
                    print("under 3 hours")
                    return data_
                else:
                    print("over 3 hours")
                    return data()
        else:
            print("no file exists")
            data_: dict = data()
            json.dump(data_, saved)
            return data_
    # TODO: refactor this


def sub_hour(before: datetime, after: datetime):
    diff = after - before
    diff_second = diff.total_seconds()
    hours = divmod(diff_second, 3600)[0]
    return hours

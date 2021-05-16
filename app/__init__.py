from flask.templating import render_template
from app.data.data import data
from datetime import datetime
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    data_ = data()
    print("Data fetched")
    if data_:
        return render_template("index.html", data=data_)
    else:
        return "Key error"


@app.template_filter("strftime")
def format_datetime(value: datetime):
    if value.hour >= 12:
        am_pm = "오후"
    else:
        am_pm = "오전"
    return value.strftime(f"%m월 %d일 {am_pm} %I시")

from flask.templating import render_template
from app.data.data import data
from datetime import datetime
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/data", methods=["POST"])
def get_data():
    return data()


@app.template_filter("strftime")
def format_datetime(value: str):
    print(value)
    time = datetime.strptime(value, r"%Y-%m-%d %H:%M:%S")
    if time.hour >= 12:
        am_pm = "오후"
    else:
        am_pm = "오전"
    return time.strftime(f"%m월 %d일 {am_pm} %I시")

from flask import Flask, render_template
import requests
import os
from requests.sessions import PreparedRequest
from parse import parse, current_time
from datetime import datetime

app = Flask(__name__)

CURRENT_TIME: datetime = current_time()
DATE = CURRENT_TIME.strftime(r"%Y%m%d")
TIME = CURRENT_TIME.strftime(r"%H00")
url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
params = {
    "ServiceKey": os.environ.get("WEATHER_API_KEY"),
    "pageNo": 1,
    "numOfRows": 70,
    "dataType": "JSON",
    "base_date": DATE,
    "base_time": TIME,
    "nx": 89,
    "ny": 111,
}
req = PreparedRequest()
req.prepare_url(url, params)
response = requests.get(req.url)
data = response.json()


@app.template_filter("strftime")
def format_datetime(value: datetime):
    if value.hour >= 12:
        ampm = "오후"
    else:
        ampm = "오전"
    return value.strftime(f"%m월 %d일 {ampm} %I시")


@app.route("/")
def index():
    return render_template("index.html", data=parse(data))


if __name__ == "__main__":
    app.run(debug=True)

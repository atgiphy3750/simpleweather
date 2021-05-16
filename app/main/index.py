from app.parse.parse import parse_data, current_time
from flask import render_template
from flask.blueprints import Blueprint
import requests
import os
from datetime import datetime


def get_data():
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    if WEATHER_API_KEY is None:
        return False

    CURRENT_TIME: datetime = current_time()
    DATE = CURRENT_TIME.strftime(r"%Y%m%d")
    TIME = CURRENT_TIME.strftime(r"%H00")

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
    params = {
        "ServiceKey": WEATHER_API_KEY,
        "pageNo": 1,
        "numOfRows": 70,
        "dataType": "JSON",
        "base_date": DATE,
        "base_time": TIME,
        "nx": 89,
        "ny": 111,
    }
    req = requests.sessions.PreparedRequest()
    req.prepare_url(url, params)
    response = requests.get(req.url)

    data = response.json()

    return data


main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
def index():
    data = get_data()
    if data:
        return render_template("index.html", data=parse_data(data))
    else:
        return "Key error"

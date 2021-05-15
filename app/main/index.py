from app.parse.parse import parse_data, current_time
from flask import Flask, render_template
from flask.blueprints import Blueprint
import requests
import os
from datetime import datetime
from dotenv import load_dotenv


def get_data():
    load_dotenv(verbose=True)

    CURRENT_TIME: datetime = current_time()
    DATE = CURRENT_TIME.strftime(r"%Y%m%d")
    TIME = CURRENT_TIME.strftime(r"%H00")

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
    params = {
        "ServiceKey": os.getenv["WEATHER_API_KEY"],
        "pageNo": 1,
        "numOfRows": 70,
        "dataType": "JSON",
        "base_date": DATE,
        "base_time": TIME,
        "nx": 89,
        "ny": 111,
    }
    print(os.environ.get("WEATHER_API_KEY"))
    req = requests.sessions.PreparedRequest()
    req.prepare_url(url, params)
    response = requests.get(req.url)
    data = response.json()

    return data


main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
def index():
    return render_template("index.html", data=parse_data(get_data()))

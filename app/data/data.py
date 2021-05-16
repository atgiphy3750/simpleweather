import os
from typing import Dict
from datetime import datetime, timedelta
import requests


SKY = ["", "맑음", "구름조금", "구름많음", "흐림"]
PTY = ["없음", "비", "비/눈", "소나기", "빗방울", "빗방울/눈날림", "눈날림"]
WEATHER = "weather"
TEMP = "temp"
CATEGORY = "category"
FORECASTDATE = "fcstDate"
FORECASTTIME = "fcstTime"
FORECASTVALUE = "fcstValue"
BASETIME = [2, 5, 8, 11, 14, 17, 20, 23]
RAIN = "rain"


def data():
    return parse(get_data())


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


def current_time():
    utctime = datetime.utcnow()
    time = utctime + timedelta(hours=9)
    time -= timedelta(minutes=5)
    while not time.hour in BASETIME:
        time -= timedelta(hours=1)
    time -= timedelta(hours=3)
    return time


def parse(data: Dict):
    result: Dict = {}
    items: Dict = data["response"]["body"]["items"]["item"]
    for item in items:
        date_str = f"{item[FORECASTDATE]}{item[FORECASTTIME]}"
        date = datetime.strptime(date_str, r"%Y%m%d%H%M")
        if result.get(date) is None and len(result) < 6:
            result[date] = {}
        category = item[CATEGORY]

        if category == "PTY":
            value = int(item[FORECASTVALUE])
            if value:
                result[date][WEATHER] = PTY[value]
        if category == "SKY":
            value = int(item[FORECASTVALUE])
            if result[date].get(WEATHER) is None:
                result[date][WEATHER] = SKY[value]
        if category == "T3H":
            value = int(item[FORECASTVALUE])
            result[date][TEMP] = value
        if category == "POP":
            value = int(item[FORECASTVALUE])
            result[date][RAIN] = value

        if (
            len(result) == 5
            and result[date].get(WEATHER)
            and result[date].get(TEMP)
            and result[date].get(RAIN)
        ):
            break

    return result
from datetime import datetime
from typing import Dict


class Weather:
    """
    Weather Class
    """

    DATETIME: str = "datetime"
    DATE: str = "date"
    RAIN: str = "rain"
    WEATHER: str = "weather"
    TEMP: str = "temp"

    PTY: str = "PTY"
    SKY: str = "SKY"
    T3H: str = "T3H"
    POP: str = "POP"

    SKYLIST = ["", "맑음", "구름조금", "구름많음", "흐림"]
    PTYLIST = ["", "비", "비/눈", "소나기", "빗방울", "빗방울/눈날림", "눈날림"]

    CATEGORY = "category"
    FCSTDATE = "fcstDate"
    FCSTTIME = "fcstTime"
    FCSTVALUE = "fcstValue"

    def __init__(self) -> None:
        self.__datetime: datetime
        self.__date: str = ""
        self.__rain: int = 0
        self.__weather: str = ""
        self.__temp: int = 0

    def add(self, data):
        category = data[Weather.CATEGORY]
        date = data[Weather.FCSTDATE]
        time = data[Weather.FCSTTIME]
        value = data[Weather.FCSTVALUE]
        if not self.__date:
            self.__datetime = self.__get_datetime(date, time)
            self.__date = str(self.__datetime.date())
        self.__set_data(value, category)

    def __set_data(self, value, type: str) -> None:
        if type == Weather.PTY:
            if value:
                self.__weather = Weather.PTYLIST[int(value)]
        elif type == Weather.SKY:
            if self.__weather == "":
                self.__weather = Weather.SKYLIST[int(value)]
        elif type == Weather.T3H:
            self.__temp = value
        elif type == Weather.POP:
            self.__rain = value

    def should_break(self) -> bool:
        return self.__is_full()

    def should_continue(self, item) -> bool:
        datetime = self.__get_datetime(item[Weather.FCSTDATE], item[Weather.FCSTTIME])
        date = datetime.date()
        return self.__is_full() and self.__date == date

    def __is_full(self) -> bool:
        if self.__date and self.__rain and self.__weather and self.__temp:
            return True
        else:
            return False

    def to_dict(self) -> Dict:
        data = {
            Weather.DATE: self.__date,
            Weather.RAIN: self.__rain,
            Weather.WEATHER: self.__weather,
            Weather.TEMP: self.__temp,
        }
        return data

    @staticmethod
    def __get_datetime(date, time):
        date_str = f"{date}{time}"
        return datetime.strptime(date_str, r"%Y%m%d%H%M")

    def __str__(self):
        return f"date: {self.__datetime}, rain: {self.__rain}, weather: {self.__weather}, temp: {self.__temp}"

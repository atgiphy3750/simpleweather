from datetime import datetime
from flask import Flask
from app.main.index import main

app = Flask(__name__)


@app.template_filter("strftime")
def format_datetime(value: datetime):
    if value.hour >= 12:
        am_pm = "오후"
    else:
        am_pm = "오전"
    return value.strftime(f"%m월 %d일 {am_pm} %I시")


app.register_blueprint(main)

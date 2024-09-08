import datetime
import requests
from functools import lru_cache


def _get_headers():
    return {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

def is_holiday(check_day:datetime.date):
    # 判断是否是节假日
    # 接口为： http://timor.tech/api/holiday/info/2024-09-08
    headers = _get_headers()
    api = 'http://timor.tech/api/holiday/info/'
    res = requests.get(url=api+str(check_day), headers=headers)
    holiday = res.json()['type']['type'] # 0 1 2 3 工作日，周末，节假日， 调休（休息日但却要上班）
    return holiday == 2

def is_weekend(check_day:datetime.date):
    # 判断是否是周末
    return check_day.weekday() >= 5 # 0 1 2 3 4  | 5 6


if __name__ == "__main__":
    day = datetime.date(2024,9, 9)
    print(day.weekday())
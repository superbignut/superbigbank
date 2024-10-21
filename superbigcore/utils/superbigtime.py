"""
    由于只有在工作日，交易所才能进行交易，因此需要一些辅助函数来进行判断

    此外，工作日的交易时间也需要进行处理

"""
import datetime
from math import trunc

import requests
from functools import lru_cache, cache



OPEN_TIME = (
    (datetime.time(9,30,0), datetime.time(11,30,0)),
    (datetime.time(13,0,0), datetime.time(15,0,0))
)



def _get_headers():
    return {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}



# 使用cache 似乎比 lru_cache更加合理
@cache
def is_holiday(check_day:datetime.date):
    # 判断是否是节假日，并进行缓存，加速下次同参数的查询;接口为： http://timor.tech/api/holiday/info/2024-09-08
    headers = _get_headers()
    api = 'http://timor.tech/api/holiday/info/'
    res = requests.get(url=api+str(check_day), headers=headers)
    ######################### 这里有问题， 总会报错 Todo
    holiday = res.json()['type']['type'] # 0 1 2 3 工作日，周末，节假日， 调休（休息日但却要上班）
    #########################
    return holiday == 2



def is_weekend(check_day:datetime.date):
    # 判断是否是周末
    return check_day.weekday() >= 5 # 0 1 2 3 4  | 5 6




def is_trade_day(check_day:datetime.date):
    # 判断是否是交易日
    return not (is_holiday(check_day) or is_weekend(check_day))



def get_next_trade_day(check_day:datetime.date, max_check_day=300):
    # 获取从check_day 开始的下一个交易日
    i = 1
    while True:
        new_day = check_day + datetime.timedelta(i) # bug_fixed 这里是应该是i，否则死循环
        if is_trade_day(new_day):
            return new_day
        else:
            i+=1
        if i > max_check_day:
            raise RuntimeError("get_next_trade_day() can't find a valid answer.")



def is_trade_time(check_time:datetime.time):
    # 判断时间是否是交易时间
    for duration in OPEN_TIME:
        if duration[0] < check_time < duration[1]:
            return True
    return False



def is_pause_time(check_time:datetime.time):
    # 判断是否是停牌时间
    return not is_trade_time(check_time)



def is_continue_time(check_time:datetime.time):
    # 是否是下午交易区间--不确定
    pass



def is_closing_time(check_time:datetime.time):
    # 是否快到关闭时间15：00
    pass



if __name__ == "__main__":
    day = datetime.date(2024,9, 9)
    if 1 < 0 < 5:
        print(is_trade_time(datetime.time(9,9,9)))

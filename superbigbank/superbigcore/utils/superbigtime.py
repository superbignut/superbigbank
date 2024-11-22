"""
    由于只有在工作日，交易所才能进行交易，因此需要一些辅助函数来进行判断

    此外，工作日的交易时间也需要进行处理

"""
import datetime
import time
from math import trunc
import os
import json
import requests
from functools import lru_cache, cache
import multiprocessing.pool


OPEN_TIME = (
    (datetime.time(9,30,0), datetime.time(11,30,0)),
    (datetime.time(13,0,0), datetime.time(15,0,0))
)

temp_year = '2024' # 当前是2024 年

HOLIDAY_JSON_PATH = os.path.join(os.path.dirname(__file__), temp_year + '.json') # 判断是不是holiday 的存储地址

def _get_headers():
    return {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}



# 使用cache 似乎比 lru_cache更加合理
@cache
def is_holiday(check_day:datetime.date):
    try:
        with open(HOLIDAY_JSON_PATH) as temp_file:
            holiday = json.load(temp_file)[str(check_day)]
    except:
        raise ValueError("If the New Year is coming, you need to take a look at the main function")
    # 判断是否是节假日，并进行缓存，加速下次同参数的查询;接口为： http://timor.tech/api/holiday/info/2024-09-08
    # headers = _get_headers()
    # api = 'http://timor.tech/api/holiday/info/'
    # res = requests.get(url=api+str(check_day), headers=headers)
    # ######################### 这里有问题， 总会报错 Todo
    # holiday = res.json()['type']['type'] # 0 1 2 3 工作日，周末，节假日， 调休（休息日但却要上班）
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

def help_map(params):
    headers = _get_headers()
    api = 'http://timor.tech/api/holiday/info/'
    while True:
        try:
            res = requests.get(url=api + str(current_date), headers=headers).json()
            if res['code'] != 0: # 可能会报错
                time.sleep(0.5)
                continue
        except:
            time.sleep(0.5) # 如果报错就从来
            continue
        else:
            return res



"""
    每到新的一年的时候， 要修改一下年份 temp_year，然后重新
    
    python __file__ (这个文件)

"""
if __name__ == "__main__":

    start_date = datetime.datetime.now().date()

    end_date = datetime.date(start_date.year, 12, 31)

    date_list = []

    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=1)

    date_list_save_dict = {}
    LENGTH = 10
    for i in range(0, len(date_list), LENGTH):
        temp_list = date_list[i : i+LENGTH]
        pool = multiprocessing.pool.ThreadPool(min(len(temp_list), os.cpu_count()))  # 多线程
        res = pool.map(help_map, temp_list)
        for index in range(len(res)):
            # print(str(temp_list[i + index]))
            date_list_save_dict[str(temp_list[index])] = res[index]['type']['type']

    with open(temp_year + '.json', 'w', encoding='utf8') as temp_f:
        temp_f.write(json.dumps(date_list_save_dict))



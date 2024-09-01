import re
import time
from functools import partial

from basedata import BaseData
from helpers import *
import multiprocessing.pool

class Tencent(BaseData):

    def __init__(self):
        super().__init__()

    @property
    def stock_api(self) -> str:
        # 返回腾讯财经的数据地址，格式为：
        # web.sqt.gtimg.cn/?q=sh600519 (,stock_code)*
        # sqt.gtimg.cn/?q=sh600519 (,stock_code)*
        # sqt.gtimg.cn/q=sh600519 (,stock_code)*
        return "https://web.sqt.gtimg.cn/?q="



if __name__ == '__main__':
    te = Tencent()
    print(te.all_market())
import re
import time
from basedata import BaseData
from helpers import *

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
    ls = ["000001", "000002", "000003", "000004", "000005", "000006", "000007", "000008", "000009", "000010","000011"]
    print(te.gen_stock_list(ls))
import re
import time
from functools import partial

from basedata import BaseData
from helpers import *
import multiprocessing.pool

class Tencent(BaseData):

    def __init__(self):
        super().__init__()
        # 如果不写构造函数，默认调用父类init，效果相同

    @property
    def stock_api(self) -> str:
        # 返回腾讯财经的数据地址，格式为：
        # web.sqt.gtimg.cn/?q=sh600519 (,stock_code)*
        # sqt.gtimg.cn/?q=sh600519 (,stock_code)*
        # sqt.gtimg.cn/q=sh600519 (,stock_code)*
        return "https://web.sqt.gtimg.cn/?q="



if __name__ == '__main__':
    te = Tencent()
    print(te.stocks(['600519', '000001']))
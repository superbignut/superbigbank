import json
import requests
from abc import ABCMeta, abstractmethod

from helpers import *



class BaseData(metaclass=ABCMeta):
    # 行情获取基类

    max_num = 10
    # 每次请求的最大股票数

    # @property
    @abstractmethod
    def stock_api(self) -> str:
        pass
    # 获取行情的api地址

    def __init__(self):
        self._session = requests.sessions.Session()
        stock_codes = self.load_stock_codes()
        self.stock_list = self.gen_stock_list(stock_codes) # 对股票代码进行分组

    def gen_stock_list(self, stock_codes : list) -> list:
        # 根据 self.max_num 为每组长度 返回用‘,'连接的list[str,]
        # 举例 max_num = 2 : ['sh600519,sz000001', 'sh600619,sz000002']
        # 对字符串进行分组的目的，是希望以组为单位对数据进行多进程获取
        stock_with_type_prefix = get_stock_list_with_type_prefix(stock_codes)
        if len(stock_with_type_prefix) <= self.max_num:
            request_list = ','.join(stock_with_type_prefix)
            return [request_list, ]

        stock_list = []
        for i in range(0, len(stock_with_type_prefix), self.max_num):
            request_list = ','.join(stock_with_type_prefix[i : i + self.max_num])
            stock_list.append(request_list)
        return stock_list



    @staticmethod
    def load_stock_codes()->list:
        # 简单的返回所有的股票代码，没有交易所前缀
        with open(STOCK_CODE_PATH) as temp_f:
            return json.load(temp_f)['stock']


    def all_market(self):
        pass


    def stocks(self):
        pass


    def market_snapshot(self):
        pass


    def get_stock_by_range(self, params):
        # 根据不同的api 与 params 获取数据， 这里的params 应该就是 'sh600519,sz000001' 的字符串
        temp_headers = self._get_headers()
        r = self._session.get(self.stock_api() + params , headers=temp_headers)
        return r.text


    @staticmethod
    def _get_headers()->dict:
        # 构造浏览器的 header
        return {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}


    def get_stock_data(self):
        pass

    def _fetch_stock_data(self):
        pass


if __name__ == '__main__':
    # print(BaseData.gen_stock_list( ) )
    pass


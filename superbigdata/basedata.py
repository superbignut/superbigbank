"""
    主要的从web中的get数据的函数是 get_stock_by_web_api，并调用了虚函数 stock_api，

     不同的子类需要完成自己的实现方法， 而 _fetch_stock_data 函数负责多线程、多进程来

     调用 get_stock_by_web_api。这里是考虑到每次网络请求可能有数量限制

     而 get_stock_data 则封装了 _fetch_stock_data 和 _format_response_data，当然

     不同的子类也许实现不同的格式化方法；

     其余的 all_market， stocks， _realtime_data， 则都是进一步封装get_stock_data的函数
"""

import json
import requests
from abc import ABCMeta, abstractmethod
import multiprocessing.pool

from .helpers import *

class BaseData(metaclass=ABCMeta):
    # 行情获取基类

    max_num = 200
    # 每次请求的最大股票数

    @property
    @abstractmethod
    def stock_api(self) -> str:
        # 所有的基类继承这个属性抽象成员函数，进而在子类的对象调用时使用子类的api
        # 在 get_stock_by_web_api 中被调用
        pass
    # 获取行情的api地址

    def __init__(self):
        self._session = requests.sessions.Session()
        stock_codes = self.load_stock_codes()
        self.stock_group_with_prefix = self._generate_stock_group_with_prefix(stock_codes) # 对股票代码进行分组

    def _generate_stock_group_with_prefix(self, stock_codes : list) -> list:
        # 根据 self.max_num 为每组长度 返回用‘,'连接的股票代码的 list[str,]
        # 举例 max_num = 2 : ['sh600519,sz000001', 'sh600619,sz000002']
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
        # 从STOCK_CODE_PATH中加载股票代码，没有交易所前缀, 这里没有调用helpers 中的重新获取函数
        # 如果 STOCK_CODE_PATH 中的数据是空的，可能要重新调用helpers.update_stock_codes()进行更新
        with open(STOCK_CODE_PATH) as temp_f:
            return json.load(temp_f)['stock']


    def all_market(self):
        # 返回所有股票的行情数据
        return self.get_stock_data(self.stock_group_with_prefix)


    def stocks(self, stock_codes):
        # 返回任意股票代码或列表的对应的实时数据, 前缀不是必须
        # 举例：['600519', '000001']
        return self._realtime_data(stock_codes)

    def _realtime_data(self, stock_codes):
        # 返回任意股票代码对应的实时数据, 前缀不是必须
        if not isinstance(stock_codes, list):
            stock_codes = [stock_codes, ]

        stock_group_with_prefix = self._generate_stock_group_with_prefix(stock_codes)  # 对股票代码进行分组

        return self.get_stock_data(stock_group_with_prefix)


    def market_snapshot(self):
        pass


    def get_stock_by_web_api(self, params:str)->str:
        # 根据不同的api 与 params 获取数据， 这里的params 应该就是 'sh600519,sz000001' 的字符串
        temp_headers = self._get_headers()
        r = self._session.get(self.stock_api + params , headers=temp_headers)
        return r.text


    @staticmethod
    def _get_headers()->dict:
        # 构造浏览器的 header
        return {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}


    def get_stock_data(self, stock_list_with_prefix:list[str]):
        # 从web 中获取股票信息
        temp_data = self._fetch_stock_data(stock_list_with_prefix)
        return self._format_response_data(temp_data)

    def _fetch_stock_data(self, stock_list:list[str], method='mutil-process')->list[str]:
        # 从web 中获取股票信息
        if method == 'mutil-process':
            pool = multiprocessing.Pool(min(len(stock_list), os.cpu_count()))  # 使用多进程会造成 self 对象被赋值到每一个进程中，
            # 具体可以体现在下面调用 get_stock_by_web_api 时 每个进程的 self均为不同的对象， 而多线程则是用一个对象
        else:
            pool = multiprocessing.pool.ThreadPool(min(len(stock_list), os.cpu_count()))  # 多线程
        try:
            ret = pool.map(self.get_stock_by_web_api, stock_list) # map 会阻塞代码，异步使用map_async
        except:
            pass
        finally:
            pool.close() # 不在对进程池中添加进程
        return ret

    def _format_response_data(self, data:list[str]):
        # 格式化web中得到的字符串
        pass

if __name__ == '__main__':
    # print(BaseData.gen_stock_list( ) )
    pass


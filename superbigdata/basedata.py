import json
import requests
from abc import ABCMeta, abstractmethod
from helpers import  STOCK_CODE_PATH



class BaseData(metaclass=ABCMeta):
    # 行情获取基类

    max_num = 800
    # 每次请求的最大股票数

    # @property
    @abstractmethod
    def stock_api(self) -> str:
        pass
    # 获取行情的api地址

    def __init__(self):
        self._session = requests.session()

    @staticmethod
    def _load_stock_code():
        with open(STOCK_CODE_PATH) as temp_f:
            return json.load(temp_f)['stock']




if __name__ == '__main__':
    pass


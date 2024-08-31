from abc import ABCMeta, abstractmethod


class BaseData(metaclass=ABCMeta):
    # 行情获取基类

    max_num = 800 # 每次请求的最大股票数

    # @property
    @abstractmethod
    def stock_api(self) -> str:
        pass
    # 获取行情的api地址


if __name__ == '__main__':
    print()
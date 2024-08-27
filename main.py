from debugpy.common.timestamp import current

from bigTsData import TsData
from bigExecute import *
from bigCsvData import CsvDataHandler
import os
import sys
from queue import Queue

# 获取数据 MyData       done
# 简单策略 MyStrategy   none
# 执行交易 MyExecute    none
# 不断优化 ...



event_queue = Queue() # 事件队列
data_handler = CsvDataHandler(event_queue_=event_queue,file_name_='local_data/IF.csv')

class MyQuant:
    def __init__(self):
        """
        数据初始化
        策略初始化
        运行初始化
        """
        self.data = TsData()    # 数据初始化
        self.ceo = None         # 执行交易ceo

        self.last_price = None
        self.current_price = None
        pass

    def run(self):
        if self.last_price is None:
            self.last_price = self.data.get_recent_data()['ASK']
            self.current_price = self.data.get_recent_data()['ASK']
            return
        else:
            self.last_price = self.current_price
            self.current_price = self.data.get_recent_data()['ASK']




if __name__ == '__main__':
    # mq = MyQuant()
    # print(mq.data.get_recent_data())
    # print(mq.data.get_recent_data()['ASK'])
    print("@@")
    print("Current python's Version is: ", sys.version)
    print("Compile Successfully!")
    print("@@")
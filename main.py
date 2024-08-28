import queue

from bigTsData import TsData
from bigExecute import *
from bigCsvData import CsvDataHandler
from bigRandomStrategy import RandomStrategy
import os
import sys
from queue import Queue

# 获取数据 MyData       done
# 简单策略 MyStrategy   none
# 交易准备 MyOrder
# 执行交易 MyExecute
# 更新持仓 MyFill
# 不断优化 ...



event_queue = Queue() # 事件队列

data_handler = CsvDataHandler(event_queue=event_queue,file_name='local_data/IF.csv') # 创建事件对象

strategy = RandomStrategy(event_queue=event_queue, data_handler=data_handler) # 创建策略对象


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
    while True:
        try:
            event = event_queue.get(block=True, timeout=3)
        except queue.Empty:
            break

        if event.type == 'MARKET':
            strategy.on_market_event(event) # 调用策略对象的处理函数

        elif event.type == 'SIGNAL':
            pass
        elif event.type == 'ORDER':
            pass
        elif event.type == 'FILL':
            pass

    print("@@")
    print("Current python's Version is: ", sys.version)
    print("Compile Successfully!")
    print("@@")















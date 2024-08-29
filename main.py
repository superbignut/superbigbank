from bigExecutor import EasyExecutor
from bigPortfolio import EasyPortfolio
from bigData import CsvDataHandler
from bigStrategy import EasyStrategy
import queue

event_queue = queue.Queue() # 事件队列

data_handler = CsvDataHandler(event_queue=event_queue,file_name='local_data/IF.csv') # 创建事件对象，描述数据来源

strategy = EasyStrategy(event_queue=event_queue, data_handler=data_handler) # 创建策略对象，描述自己的策略

portfolio = EasyPortfolio(event_queue=event_queue, data_handler=data_handler) # 创建组合对象，描述自己的资本

executor = EasyExecutor(event_queue=event_queue, data_handler=data_handler) # 创建交易对象， 完成实际交易




if __name__ == '__main__':
    print("Compile Successfully!")

    data_handler.run() # 启动数据接口

    while True:
        try:
            event = event_queue.get(block=True, timeout=3)
        except queue.Empty:
            break

        if event.type == 'MARKET':
            strategy.on_market_event(event) # 调用策略对象的处理函数

        elif event.type == 'SIGNAL':
            portfolio.on_signal_event(event) # 调用投资组合对象处理订单

        elif event.type == 'ORDER':
            executor.on_order_event(event)

        elif event.type == 'FILL':
            portfolio.on_fill_event(event)
















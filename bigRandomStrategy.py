from bigCore import Strategy, SignalEvent
from queue import  Queue
from bigCsvData import CsvDataHandler

import random
import time

class RandomStrategy(Strategy):

    def __init__(self, event_queue, data_handler):
        self._event_queue = event_queue
        self._data_handler = data_handler

    def on_market_event(self, event):
        """process function"""
        if event.type == "MARKET":
            # print("##################### Strategy Simulation Generation ########################")
            current_data = self._data_handler.get_current_bar()
            print("### strategy on_market_event ###", 'open price is: ', current_data['open'], time.ctime(time.time())[11:-5])

            signal_event = SignalEvent(symbol='IF', timestamp=time.time(), signal_direction=0)

            self._event_queue.put(signal_event) # 消耗 MARKET 生成 SIGNAL

if __name__ == '__main__':
    q = Queue()
    a = CsvDataHandler(event_queue=q, file_name='local_data/IF.csv', duration=1)

    s = RandomStrategy(q, a)
    a.run()




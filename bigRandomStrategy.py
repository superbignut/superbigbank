from bigCore import Strategy
from queue import  Queue
from bigCsvData import CsvDataHandler

import random

class RandomStrategy(Strategy):

    def __init__(self, event_queue, data_handler):
        self._event_queue = event_queue
        self._data_handler = data_handler

    def on_market_event(self, event):
        """process function"""
        if event.type == "MARKET":
            pass



if __name__ == '__main__':
    q = Queue()
    a = CsvDataHandler(event_queue=q, file_name='local_data/IF.csv', duration=1)

    s = RandomStrategy(q, a)
    a.run()




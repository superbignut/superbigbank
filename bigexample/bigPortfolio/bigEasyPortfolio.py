from bigexample.bigCore import Portfolio, OrderEvent
import time

class EasyPortfolio(Portfolio):

    def __init__(self, event_queue, data_handler):
        self._event_queue = event_queue
        self._data_handler = data_handler


    def on_signal_event(self, event):
        if event.type == 'SIGNAL':
            # print("##################### Portfolio Simulation Generation ########################")
            print("### portfolio on_signal_event ###", time.ctime(time.time())[11:-5])
            order_event = OrderEvent(symbol=event.symbol,
                                     timestamp=time.time(),
                                     order_type='MKT',
                                     direction=event.signal_direction,
                                     quantity=1,
                                     price=0.0)
            self._event_queue.put(order_event)

    def on_fill_event(self, event):
        print("### portfolio on_fill_event ###", time.ctime(time.time())[11:-5])
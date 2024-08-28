from bigCore import Executor, FillEvent
import time

class EasyExecutor(Executor):
    def __init__(self, event_queue, data_handler):
        self._event_queue = event_queue
        self._data_handler = data_handler

    def on_order_event(self, event):

        if event.type == "ORDER":
            print("### executor on_order_event ###", time.ctime(time.time())[11:-5])
            fill_event = FillEvent(symbol=event.symbol,
                                   timestamp=time.time(),
                                   direction=event.direction,
                                   quantity=event.quantity,
                                   price=event.price,
                                   commission=0.0,
                                   fill_flag='FAILED')
            self._event_queue.put(fill_event)
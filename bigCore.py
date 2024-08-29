from abc import ABCMeta, abstractmethod

class DataHandler(metaclass=ABCMeta):

    @abstractmethod
    def get_pre_bars(self, n=1):
        raise NotImplementedError("get_pre_bars method must be implemented!")

    @abstractmethod
    def get_current_bar(self):
        raise NotImplementedError("get_current_bars method must be implemented!")

class Strategy(metaclass=ABCMeta):

    @abstractmethod
    def on_market_event(self, event_):
        raise NotImplementedError("on_market_event method must be implemented!")


class Portfolio(metaclass=ABCMeta):

    @abstractmethod
    def on_signal_event(self, event):
        raise NotImplementedError("on_signal_event method must be implemented!")

    @abstractmethod
    def on_fill_event(self, event):
        raise NotImplementedError("on_fill_event method must be implemented!")

class Executor(metaclass=ABCMeta):
    @abstractmethod
    def on_order_event(self, event):
        raise NotImplementedError("on_order_event method must be implemented!")


class Event:
    pass

class MarketEvent(Event):
    """Generate MarketEvent by DataHandler when calling DataHandler.run()"""
    def __init__(self):
        self.type = "MARKET"

class SignalEvent(Event):
    """Consume MarketEvent() and Generate SignalEvent() by Strategy.on_market_event()"""
    def __init__(self, symbol, timestamp, signal_direction):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.timestamp = timestamp
        self.signal_direction = signal_direction

    def __repr__(self):
        print("unfinished!")


class OrderEvent(Event):
    """Consume SignalEvent() and Generate OrderEvent() by Portfolio.on_signal_event()"""
    def __init__(self, symbol, timestamp, order_type, direction, quantity, price=0.0):
        self.type = "ORDER"
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.price = price

class FillEvent(Event):
    """Consume OrderEvent() and Generate FillEvent() by Executor.on_order_event()"""
    """FillEvent is then consumed by portfolio.on_fill_event()"""
    def __init__(self, symbol, timestamp, direction, quantity, price, commission, fill_flag):
        self.type = "FILL"

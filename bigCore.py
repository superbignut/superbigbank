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


class Event:
    pass

class MarketEvent(Event):
    """
    从数据接口获得数据后生成 market 事件
    """
    def __init__(self):
        self.type = "MARKET"

class SignalEvent(Event):
    """
    由策略 生成的 交易信号 :总持仓 100
    """
    def __init__(self):
        self.type = "SIGNAL"

class OrderEvent(Event):
    """
    根据实际的情况 和 交易信号 可以交易的金额或数量 : 已有20， 再加仓80
    """
    def __init__(self):
        self.type = "ORDER"

class FillEvent(Event):
    """
    得到的真实成交的金额或数量 : 只成功交易70
    """
    def __init__(self):
        self.type = "FILL"

"""
    event 为事件基类，特殊的事件要继承Event

    event_engine 为事件引擎，包括取出事件，注册事件，插入事件等操作的接口

    具体内部实现为一个 线程安全队列 Queue

    push_engine 为多种可以向engine 中推送事件的 其他事件引擎

"""


from .push_engine import dafault_data_engine, clock_engine
from . import event_engine, event
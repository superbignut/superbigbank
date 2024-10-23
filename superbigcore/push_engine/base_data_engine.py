"""
    BaseDataEngine 作为所有 数据（产生）事件 的基类，成员函数实现了，将得到的

    数据插入 event_engine的（push_data），开始、中止等功能，只将获取数据的接口

    （fetch_data）暴露出去，不同的子类，需要实现不同的 fetch_data

    BaseDataEngine 和 Event_Engine 都使用 is_active 来控制子线程的运行，

    如果子线程中只读，而只有主线程会进行修改，那么似乎没有冲突问题，可以使用

"""

import threading
import time

from ..event import Event
from ..event_engine import EventEngine


class MarketEvent(Event):
    def __init__(self, event_type, data):
        super().__init__(event_type)
        self.data = data
# 这里新增了 MarketEvent 事件 用来和 Event 事件进行区分 clock 事件同理


class BaseDataEngine:

    EventType = "base_data_type" # 这里的EventType 是在把数据事件 put 进__queue时使用的 event_type
                                 # 可以在子类中进行重载

    # PushInterval = 1 # 每次向__queue 中 put 数据后的等待时间

    def __init__(self, event_engine, clock_engine, log, push_interval=1):
        self.event_engine = event_engine # 向 EventEngine 中推入数据
        # self.clock_engine = clock_engine # 暂时未使用
        self.log = log
        self.__thread_active = False
        self.data_thread = threading.Thread(target=self.push_data, name="BaseDataEngine", daemon=False) # 需要等待
        # daemon 默认就都是False
        self.push_interval = push_interval

    def start(self):
        # 启动子线程
        self.__thread_active = True
        self.data_thread.start()

    def stop(self):
        # 停止
        self.__thread_active = False
        self.data_thread.join()
        self.log.info("data engine closed.")

    def push_data(self):
        # 通过调用子类的 fetch_data 获得数据， 并封装为 Event事件，插入到__queue中，完成后 wait
        while self.__thread_active:
            try:
                response_data = self.fetch_data()  # 这里应该也会耗时
            except:
                self.wait()
                continue
            event = MarketEvent(event_type=self.EventType, data=response_data)
            self.event_engine.put(event) # 把 事件 put 进 __queue
            self.wait() # 每次 put 后的等待

    def wait(self):
        # 等待PushInterval, 再进行下一次获取数据
        for _ in range(self.push_interval):
            time.sleep(1)

    def fetch_data(self):
        # 子类需要时间的数据获取接口， 这里就没使用 ABC的形式
        raise NotImplementedError



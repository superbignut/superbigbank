"""
    main_engine包含了对时钟引擎，数据引擎，log，事件引擎的整合


"""
from collections import OrderedDict
from threading import Thread, Lock
from superbigcore.event_engine import EventEngine
from superbigcore.push_engine.clock_engine import ClockEngine
from superbigcore.push_engine.dafault_data_engine import DefaultDataEngine
from superbigcore.utils.superbiglog import DefaultLog


class MainEngine:
    def __init__(self, log_engine=DefaultLog(), data_engine=None, broker='xq'):
        self.log = log_engine
        self.broker = broker

        if broker is not None:
            pass

        self.event_engine = EventEngine() # 事件引擎
        self.clock_engine = ClockEngine(event_engine=self.event_engine) # 时钟引擎

        data_engines = data_engine or [DefaultDataEngine] # 这里的数据引擎 可以有多个的吗？

        if type(data_engines) != list:
            data_engines = [data_engines]
        else:
            types = [data_eng.EventType for data_eng in data_engines]
            if len(types) != len(set(types)): # 有重复
                raise ValueError("two same data_engines were added.")
        self.data_engines = [] # 数据引擎

        for engine in data_engines:
            self.data_engines.append(engine(event_engine=self.event_engine, clock_engine=self.clock_engine))

        self.strategies = OrderedDict() # dict 也具有 ordered 的能力了
        self.strategy_list = list()

        self.lock = Lock()

        self._watch_thread =None

        self.before_shutdown = []
        self.main_shutdown = []
        self.after_shutdown = []

        self.log.info("start the main engine")



"""
    main_engine包含了对时钟引擎，数据引擎，log，事件引擎等子引擎的整合

    比如整合所有的start函数， stop函数， 可以统一打开和关闭

    此外需要完成的内容是从策略目录中加载不同的策略对象

    main_engine 中 可以有多个数据引擎和策略对象

"""
import importlib
import os
import threading
import time
from collections import OrderedDict
from threading import Thread, Lock
import superbigbull

from superbigcore.event_engine import EventEngine
from superbigcore.push_engine.clock_engine import ClockEngine
from superbigcore.push_engine.dafault_data_engine import DefaultDataEngine
from superbigcore.utils.superbiglog import DefaultLog

class MainEngine:
    def __init__(self, log_engine=DefaultLog(), data_engine=None, broker='fake'):
        self.log = log_engine
        self.broker = superbigbull.use(broker) # 使用fake交易商， 传递给策略对象，用于获取持有信息，并进行交易api调用

        self.event_engine = EventEngine() # 事件引擎
        self.clock_engine = ClockEngine(event_engine=self.event_engine) # 时钟引擎

        data_engines = data_engine or [DefaultDataEngine] # 这里的数据引擎 可以有多个的吗？

        if type(data_engines) != list:
            data_engines = [data_engines]
        else:
            types = [data_eng.EventType for data_eng in data_engines]
            if len(types) != len(set(types)): # 检测数据引擎是否有重复
                raise ValueError("two same data_engines were added.")
        self.data_engines = [] # 数据引擎

        for engine in data_engines:
            self.data_engines.append(engine(event_engine=self.event_engine, clock_engine=self.clock_engine))

        self.strategy_list = list() # 把所有的策略对象加载进来
        self.strategy_class_dict = dict() # 存储名字到 类的字典
        self.strategy_folder = 'superbigsttg'  # 策略的存放路径

        # self._modules = {} #  文件名 : module  在load 函数中 加载进来

        # self.lock = Lock() 暂不使用

        # self.is_watch_strategy = False # 动态加载策略 # 暂不使用
        # self._watch_thread = Thread(target=self._load_strategy, name="MainEngine._watch_thread") # 加载策略的进程

        # self._names = None #  加载策略使用，用于记录所有需要用到的策略文件的名字

        # self.before_stop = [] #这连个应该暂时没有用到 也就是在关闭前和关闭后需要执行的操作
        self.main_stop = [] # 所有的引擎stop 函数
        # self.after_stop = []

        self.log.info("start the main engine")

    def start(self):
        # 启动 main 引擎，但这个start 应该要等到所有的handler注册之后才行

        self.event_engine.start() # 启动
        self._add_main_stop(self.event_engine.stop) # 注册事件引擎关闭

        for data_engine in self.data_engines:
            data_engine.start() # 启动
            self._add_main_stop(data_engine.stop) # 注册数据引擎关闭

        self.clock_engine.start() # 启动
        self._add_main_stop(self.clock_engine.stop) # 注册时钟引擎关闭


    def _add_main_stop(self, func):
        # 把所有的子引擎的 stop 函数 注册到self.main_stop中
        if not hasattr(func, '__call__'):
            raise ValueError("register a wrong stop func.")
        self.main_stop.append(func)


    def stop(self):
        # main_engine 的关闭， 需要把其余的有关的子引擎全部关闭
        self.log.debug("main engine is stopping.")
        for func in self.main_stop:
            func()
        num = threading.active_count()
        while threading.active_count() != num: # 这是什么意思呢？？
            time.sleep(2)
        # 还要关闭策略？？

    def load_strategy(self, names:list):
        # 从策略目录中加载 names 中指定名字的多个策略，具体加载在load()函数中
        strategy_files = os.listdir(self.strategy_folder) #
        strategy_files = filter(lambda x : x.endswith('.py') and x != '__init__.py', strategy_files) # 找到所有策略

        for file in strategy_files: # 遍历剩下的文件
            self.load(file, names) # 加载所有的策略

    def load(self, strategy_file, names:list):
        # 加载文件中的策略， 保存策略类和创建的策略对象
        # strategy_file 是策略目录中 策略文件的名字 .py结尾
        strategy_module_name = strategy_file[:-3] # 去掉 .py
        new_module = importlib.import_module('.' + strategy_module_name, package=self.strategy_folder)  # 相对导入
        strategy_class = getattr(new_module, 'Strategy') # 找到模块中的Strategy 类

        if strategy_class.name in names: # 查看策略的名字是否 在names中
            self.strategy_class_dict[strategy_class.name]= strategy_class # 存策略类
            temp_strategy = strategy_class(main_engine=self) # 创建策略对象， 这里调用策略对象的构造函数
            self.strategy_list.append(temp_strategy) # 保存策略对象

            self.strategy_listen_event_register(temp_strategy) # 把所有的时钟和数据事件绑定给策略， 具体怎么使用 由策略来决定
            self.log.info("Load Strategy: ", strategy_class.name) # 打印

    def strategy_listen_event_register(self, strategy, _type='register'):
        # 把时钟事件和数据事件，全都注册到event_engine 中
        func = {
            'register' : self.event_engine.register,
            'unregister' : self.event_engine.unregister
        }.get(_type) # 注册还是解注册

        for data_engine in self.data_engines:
            func(event_type=data_engine.EventType, handler=strategy.run) # 注册或者解注册数据事件

        func(event_type=self.clock_engine.EventType, handler=strategy.run) # 注册或解注册时钟事件



















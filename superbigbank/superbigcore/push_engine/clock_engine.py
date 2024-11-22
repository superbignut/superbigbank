"""
    ClockEngine 作为时钟引擎，主要负责在合适的时间 将ClockEvent事件插入到 event_engine当中

    主要的实现方法是 维护两个列表， 列表中的成员 分别是 ClockIntervalHandler 和 ClockMomentHandler 两种类型

    遍历并实时检查 当前的这个handler 是否被激活，激活就进行处理并 生成一个 ClockEvent事件

    使用 __thread_active 来控制线程，具体的检测和执行操作在_tick 之中进行，

    还有一些变量的设置 和 一些条件的判断还需要优化，但目前执行interval事件是没有问题的，可以成功推送到主引擎当中

    变量包括 sleep_time ,trading_state 的使用需要进一步确定
"""
import datetime
import threading
import time
from collections import deque
from queue import Queue
from  ..event_engine import EventEngine
from dateutil import tz

from ..utils import superbigtime as sutime
from ..event import Event


class ClockEvent(Event):
    def __init__(self, trading_state, clock_type:str, event_type):
        super().__init__(event_type)
        self.trading_state = trading_state # 作为一个时钟事件的全局标致位，只有在clock_engine 的注册的open close 等函数中进行修改
        # 除标记当下是否是交易时间段外，没有其他含义和功能
        self.clock_type = clock_type # 区分不同的时钟事件类型


class ClockIntervalHandler:
    # 每隔固定的间隔(分钟), 要进行触发的处理类
    def __init__(self, clock_engine, interval:int, call=None, clock_type:str=""):
        self.clock_engine = clock_engine
        self.interval = interval
        self.seconds = interval * 60 # 触发的间隔 以分钟为基本单位
        self.call = call or (lambda: None)
        self.clock_type = clock_type  # 标记这个clock_handler 的类型

        # self.last_quotient = int(self.clock_engine.now) // self.seconds # 采用求商的计算方法会从下一个seconds周期开始active


    def is_active(self):
        # 判断当下的 ClockIntervalHandler 是否处于激活状态
        return int(self.clock_engine.now % self.seconds) == 0 # 整点返回 true
        # 除非可以确定没有大于1s的延迟，否则可能会出问题
        # new_quotient = int(self.clock_engine.now) // self.seconds # 取商之前要先int
        # if new_quotient > self.last_quotient:
        #     self.last_quotient  = new_quotient
        #     return True
        # else:
        #     return False


class ClockMomentHandler:
    # 每天固定时刻的触发类

    def __init__(self, clock_engine, moment:datetime.time, call=None, clock_type:str=""):
        self.clock_engine = clock_engine
        self.moment = moment # 触发的时刻
        self.call = call or (lambda : None)
        self.clock_type = clock_type # 标记这个clock_handler 的类型

        self.next_time = datetime.datetime.combine(
            self.clock_engine.now_dt.date(),
            self.moment
        ) # 获取当天的日期,并设定处理时间

        if self.is_active(): # 如果当天的设定时间已经过了,则更新到下一个交易日
            self.update_next_time()


    def is_active(self):
        # 判断现在的时间是否可以触发 时刻对象 ClockMomentHandler
        # 此外还用来再初始化事件的时候进行判断，如果今天的时间已经过了，则更新到下一天
        return self.next_time <= self.clock_engine.now_dt # 最开始是>, 符号变为<=时触发交易


    def update_next_time(self):
        # 如果最开始设定时时间已经过了, 或者每一次成功触发后, 都会进行更新, 更新到下一个有效交易日
        if self.is_active():
            next_date = sutime.get_next_trade_day(self.next_time.date()) + datetime.timedelta(days=1)

            self.next_time = datetime.datetime.combine(
                next_date,
                self.moment
            )


class ClockEngine:
    """
        时钟引擎，负责初始化通用的时刻时间和间隔事件，并维护一个时钟线程，每次去检查所有注册的事件中

        是否有当下应该处理的，如果有的话，则创建时钟事件 ClockEvent 推送到 event_engine当中

        push_event_type 为推送函数

        _tick() 为每个时刻触发的 检测函数

        register_moment 和 register_interval 为注册函数，负责注册 各种时钟事件

    """
    EventType = 'time_tick_type' # 与事件引擎的 EventType 一样 ，作用是用来区分clock 和 data 这两种大类的数据
    # 具体的大类 Event 内部的 不同的事件， 则需要进一步区分了

    def __init__(self, event_engine:EventEngine, time_zone_info=None, sleep_time=1):
        # self.time_zone_info = time_zone_info or tz.tzlocal() # 这里是返回了一个 tzlocal 对象， 暂未使用
        self.event_engine = event_engine
        self.__thread_active = False # 线程启动、关闭标志
        self.clock_engine_thread = threading.Thread(target=self.clock_tick, name="ClockEngine.clock_tick")
        self.sleep_time = sleep_time # 每次休息1s

        self.trading_state = False # 当下是否是可以进行交易的状态,只包括对24h时间的判断，不判断是否是交易日

        self.clock_moment_handlers = deque() # 时刻的处理函数 deque 多了一层排序 # 双向队列
        self.clock_interval_handlers = set() # 时间间隔的处理函数

        self.init_clock_handler()


    def init_clock_handler(self):
        # 注册默认的时钟事件
        def _open():
            self.trading_state = True
        def _close():
            self.trading_state = False

        # 注册四个开始、暂停、继续、关闭 固定时刻的处理事件
        self.register_moment(moment=datetime.time(hour=9,minute=30),call=_open, clock_type="open") # 这里没有成功打开 fuck
        self.register_moment(moment=datetime.time(hour=11,minute=30), call=_close, clock_type="pause")
        self.register_moment(moment=datetime.time(hour=13), call=_open, clock_type="continue")
        self.register_moment(moment=datetime.time(hour=15), call=_close, clock_type="close")

        # 注册间隔事件
        for interval in (0.5, 1, 5, 15, 30, 60):
            self.register_interval(interval, clock_type=str(interval)) # interval事件没有call 函数

    def start(self):
        # 线程启动
        self.__thread_active = True
        self.clock_engine_thread.start()


    def stop(self):
        # 线程停止
        self.__thread_active = False
        self.clock_engine_thread.join()
        print("clock engine closed.")


    def clock_tick(self):
        # 线程主函数
        while self.__thread_active:
            self.tick()
            time.sleep(self.sleep_time) # sleep


    def tick(self):
        #  封装了 _tick 增加了一个 is_trade_day的判断，其实可以去掉
        if not sutime.is_trade_day(self.now_dt.date()):
            print("不是交易日，时钟引擎不处理时钟事件")
            pass
        else:
            self._tick()

    def _tick(self):
        # 为每个注册的 并处在 active 状态的 handlers 完成一次处理
        # 处理间隔事件
        for handler in self.clock_interval_handlers:
            if handler.is_active():
                handler.call()
                self.push_event_type(handler.clock_type) # 每次只需要把 clock_type写进去即可

        # 处理时刻事件, 其实时刻处理应该更靠前一点
        while self.clock_moment_handlers:
            clock_handler = self.clock_moment_handlers.popleft() # 左边是最小的时间对应的事件
            if clock_handler.is_active(): # 这种每次都要检查的机制
                clock_handler.call()
                self.push_event_type(clock_handler.clock_type) # 将对应的事件插入 event_engine中
                clock_handler.update_next_time() # 更新下一个事件，一天之后
                self.clock_moment_handlers.append(clock_handler) # 放回deque 的右边
            else:
                self.clock_moment_handlers.appendleft(clock_handler) # 如果没有被激活，就还放回最左边，这里是因为是时刻事件
                # 所以如果最小的没有被激活，大的肯定也没有激活
                break # queue为空或最小的事件没有激活则跳出循环


    def push_event_type(self, clock_type): # 这里其实传入type 就行不需要传入handler
        # 把handler ClockEvent 事件， 插入到事件引擎当中
        event = ClockEvent(event_type=self.EventType, trading_state=self.trading_state, clock_type=clock_type)
        print("come in.")
        self.event_engine.put(event)


    def register_moment(self, moment:datetime.time, call=None, clock_type=""):
        # 注册时刻处理函数, 并对所有的 deque 中的 handler 从大到小进行入队
        handlers = list(self.clock_moment_handlers)
        handler = ClockMomentHandler(self, moment, call, clock_type)

        handlers.append(handler)

        handlers.sort(key=lambda x : x.next_time, reverse=False) # 从小到大
        self.clock_moment_handlers = deque(handlers)

        return handler


    def register_interval(self, interval:int, call=None, clock_type=""):
        # 注册间隔处理函数
        handler = ClockIntervalHandler(self, interval, call, clock_type)
        self.clock_interval_handlers.add(handler)
        return handler


    @property
    def now(self)->float:
        return time.time()


    @property
    def now_dt(self)->datetime.datetime:
        # arrow 库
        # return arrow.get(time.time()).to(tz.tzlocal()) # 这个应该是可以加上地区
        return datetime.datetime.now() # datetime 应该也是可以的



"""
    Clock



"""
import time
import datetime
from collections import deque
import arrow
import threading
from ..utils import superbigtime as mytime
from .. import event
from  dateutil import tz

from ..utils.superbigtime import get_next_trade_day


class Clock:
    pass


class ClockIntervalHandler:
    # 每隔固定的间隔(分钟), 要进行触发的处理类

    def __init__(self, clock_engine, interval:int, call=None):
        self.clock_engine = clock_engine
        self.interval = interval
        self.seconds = interval * 60 # 触发的间隔 以分钟为基本单位
        self.call = call or (lambda: None)
        self.last_quotient = int(self.clock_engine.now) // self.seconds # 采用求商的计算方法会从下一个seconds周期开始active


    def is_active(self):
        # 判断现在的时间是否可以触发
        if not self.clock_engine.trading_state: # 意义不确定
            return False
        # return int(self.clock_engine.now % self.seconds) == 0 # now 这种判断方法有可能会跳过处理时间
        new_quotient = int(self.clock_engine.now) // self.seconds # 取商之前要先int
        if new_quotient > self.last_quotient:
            self.last_quotient  = new_quotient
            return True
        else:
            return False


class ClockMomentHandler:
    # 每天固定时刻的触发类

    def __init__(self, clock_engine, moment:datetime.time, call=None):
        self.clock_engine = clock_engine
        self.moment = moment # 触发的时刻
        self.call = call or (lambda : None)
        self.next_time = datetime.datetime.combine(
            self.clock_engine.now_dt.date(),
            self.moment
        ) # 获取当天的日期,并设定处理时间

        if self.is_active(): # 如果当天的设定时间已经过了,则更新到下一个交易日
            self.update_next_time()


    def is_active(self):
        # 判断现在的时间是否可以触发
        if not self.clock_engine.trading_state:  # 是否? 这里需要进一步处理
            return False
        return self.next_time <= self.clock_engine.now_dt # 最开始是>, 符号变为<=时触发交易


    def update_next_time(self):
        # 如果最开始设定时时间已经过了, 或者每一次成功触发后, 都会进行更新, 更新到下一个有效交易日
        if self.is_active():
            next_date = get_next_trade_day(self.next_time.date()) + datetime.timedelta(days=1)

            self.next_time = datetime.datetime.combine(
                next_date,
                self.moment
            )


class ClockEngine:
    EventType = 'time_tick'

    def __init__(self, event_engine, time_zone_info=None):
        self.time_zone_info = time_zone_info or tz.tzlocal()
        self.event_engine = event_engine
        self.is_active = False
        self.clock_engine_thread = threading.Thread(target=self.clock_tick, name="ClockEngine.clock_tick")
        self.sleep_time = 1

        self.trading_state = False # 当下是否是可以进行交易的状态,可能是 非交易日或 交易日的非交易时间段

        self.clock_moment_handlers = deque() # 时刻的处理函数
        self.clock_interval_handlers = set() # 时间间隔的处理函数

        self.init_clock_handler()


    def init_clock_handler(self):
        # 注册默认的时钟事件
        pass


    def clock_tick(self):
        while self.is_active:
            self.tick()
            time.sleep(self.sleep_time)


    def tick(self):
        # tick() 函数相当于一个处理流程，所有的注册的, 并处在 active 状态的 handlers 完成一次处理
        if not mytime.is_trade_day(self.now_dt):
            pass
        else:
            self._tick()


    def _tick(self):
        # 为每个注册的 并处在 active 状态的 handlers 完成一次处理
        # 处理间隔事件
        for handler in self.clock_interval_handlers:
            if handler.is_active():
                pass

        # 处理时刻事件
        while self.clock_moment_handlers:
            clock_handler = self.clock_moment_handlers.pop()
            pass


    def register_moment(self):
        # 注册时刻处理函数
        pass


    def register_interval(self):
        # 注册间隔处理函数
        pass


    @property
    def now(self)->float:
        return time.time()


    @property
    def now_dt(self)->datetime.datetime:
        # arrow 库
        # return arrow.get(time.time()).to(tz.tzlocal()) # 这个应该是可以加上地区
        return datetime.datetime.now() # datetime 应该也是可以的



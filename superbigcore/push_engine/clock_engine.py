"""
    Clock



"""
import threading


from superbigcore import event

from  dateutil import tz


class Clock:
    pass


class ClockIntervalHandler:
    pass


class ClockMomentHandler:
    pass


class ClockEngine:
    EventType = 'time_tick'

    def __init__(self, event_engine, time_zone_info=None):
        self.time_zone_info = time_zone_info or tz.tzlocal()
        self.event_engine = event_engine
        self.is_active = False
        self.clock_engine_thread = threading.Thread(target=self.clocktick, name="ClockEngine.clocktick")
        self.sleep_time = 1


        self.init_clock_handler()

    def init_clock_handler(self):
        # 注册默认的时钟事件
        pass

    def clocktick(self):
        pass




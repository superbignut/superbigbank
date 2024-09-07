"""
    Clock



"""
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

    def __init__(self, event_engine, tzinfo=None):
        self.tzinfo = tzinfo or tz.tzlocal()
        self.event_engine = event_engine
        self.is_active = False





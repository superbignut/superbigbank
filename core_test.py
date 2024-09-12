import datetime

import arrow

from superbigdata import *
from superbigcore import *
import json
import time
from dateutil import tz

if __name__ == '__main__':
    main_engine = event_engine.EventEngine()
    main_engine.register('clock_tick', lambda x: print(x))
    clock = clock_engine.ClockEngine(main_engine)
    main_engine.start()
    clock.start()
    print("Compile Successfully!")

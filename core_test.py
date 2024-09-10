import datetime

import arrow

from superbigdata import *
from superbigcore import *
import json
import time
from dateutil import tz

if __name__ == '__main__':
    co = clock_engine.ClockEngine(1)
    print(co.now_dt.time())
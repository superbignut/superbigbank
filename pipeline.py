import datetime
import threading

import arrow
import sys
import traceback
from superbigcore.main_engine import MainEngine
from superbigcore.push_engine.base_data_engine import BaseDataEngine
from superbigcore.utils.superbiglog import DefaultLog
import superbigdata
import importlib
import json
import time
from dateutil import tz

class TestDataEngine(BaseDataEngine):
    # 如果只是使用具体的几个股票数据，可以自定义数据引擎 ， 重载init和fetch函数

    def __init__(self, event_engine, clock_engine):
        super().__init__(event_engine, clock_engine, push_interval=1)
        self.source = superbigdata.use('sina')

    def fetch_data(self):
        return self.source.stocks(['600519', '000001'])


if __name__ == '__main__':

    robot = MainEngine()
    robot.load_strategy(['strategy_example'])

    print(robot.strategy_list)







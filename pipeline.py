import datetime
import threading
import multiprocessing # 真想利用就多进程吧
import arrow
import sys
import traceback
from superbigcore.main_engine import MainEngine
from superbigsttg.strategy_example import SmallDataEngine
from superbigcore.push_engine.base_data_engine import BaseDataEngine
from superbigcore.utils.superbiglog import DefaultLog
import superbigdata
import importlib
import json
import time
from dateutil import tz


if __name__ == '__main__':

    robot = MainEngine(data_engine=SmallDataEngine, broker='fake') # 创建主引擎
    robot.load_strategy(['strategy_example']) # 加载策略列表
    robot.start() # 主引擎启动










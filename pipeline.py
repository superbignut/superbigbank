"""
    pipeline.py 作为一份使用实例，包括了使用 superbigbank 的核心逻辑

    安装好依赖后，python pipeline.py 运行文件， Ctrl + C 结束， 可视化部分正在添加
"""

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
    # 使用 Ctrl + C 结束 所有引擎
    robot = MainEngine(data_engine=SmallDataEngine, broker='fake') # 创建主引擎
    robot.load_strategy(['strategy_example']) # 加载策略列表
    robot.run() # 主引擎启动
    # 可视化启动 应该就是放到 brocker 里面








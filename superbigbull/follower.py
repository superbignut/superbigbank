"""
    计划有变，打算自己写一个虚拟交易， 或者是弄一个线程，或者就是一个简单的函数，

    把 延时等待，滑点， 手续费，模拟出来就可以了

    等到真要真实交易的时候，直接上 easytrader 的 模拟点击吧
"""

import abc
from queue import Queue
import requests

class BaseFollower(metaclass=abc.ABCMeta):
    # 跟踪器


    LOGIN_PAGE = "" # 登录界面
    LOGIN_API = "" # 登录api
    TRANSACTION_API = "" # 交易api

    WEB_REFERER = "" # 暂不理解
    WEB_ORIGIN = "" # 暂不理解

    def __init__(self):
        self.trade_queue = Queue()
        self.expired_cmds = set() # 过期指令？
        self.session = requests.Session() # 创建 Session
        self.session.verify = False # 这是什么
        self.slippage:float = 0.8 # 滑点


    def log_in(self, user=None, password=None, *args, **kwargs):
        headers = self._get_headers()
        self.session.headers.update(headers)

    def _get_headers(self):
        pass


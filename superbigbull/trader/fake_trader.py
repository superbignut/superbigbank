"""
    这是一个假的 交易对象， 提供基本的买卖函数， 先越简单越好，

    然后的话， 应该是把数据引擎再次获取， 并且和交易信息全都可视化到网页端，

    与可视化进程之间的通信方式，暂时使用的是读写data.json文件

"""
import multiprocessing
import threading
import time
import json
import os
import subprocess
from filelock import FileLock
from collections import defaultdict

LOCK_FILE_ADDR = os.path.join(os.path.dirname(__file__), "data.json.lock")
IPC_FILE_ADDR = os.path.join(os.path.dirname(__file__), "data.json")

json_data_lock = FileLock(LOCK_FILE_ADDR, timeout=2) # 把数据写到json中 之前需要先拿到锁
"""
    但是由于我是在windows上写的代码，测试两个进程同时分别读写进程，也没有问题出现，在os似乎已经被加了锁
"""

BULL= {'BUY':0, "SELL":1} # 买卖方向

class OneDeal:
    # 一笔交易的类型， 时间，名字，数量，买卖方向
    def __init__(self, time, name, num, direction):
        pass

def update_after_trade_decorator(trade_function):
    # 修饰器函数，用于修饰FakeTrader 的交易函数, 在交易后更新可视化数据
    def wrapper(self, *args, **kwargs):
        # FakeTrader类的一些成员函数
        result = trade_function(self, *args, **kwargs)  # 交易函数
        self.trade_data_update()  # 可视化更新
        return result  # 如果有结果，返回
    return wrapper


class FakeTrader:
    # 虚假的交易商， 会扣除你非常多的手续费
    def __init__(self, init_money=1_000_000, log=None):

        # self.update_thread_flag = False # 数据提交线程控制位
        # self.update_thread = threading.Thread(target=self.trade_data_update, name="Fake_Trader_update_thread")
        self.log = log
        self.st_show_process = None # 可视化进程 用于安全关闭
        self.stock_dict = defaultdict(int) # 600519 : 持有数量
        self.fund_data_dict = {
            "initial_fund": 0.0,  # 投入资金
            "existing_fund": 0.0, # 现有资金
            "total_assets": 0.0, # 全部资产总和 = 现有资金 + 股票
            "current_time":0 # 当下的时间
        }
        self._add_money_to_account(init_money) # 初始化资金

    def start(self):
        # self.update_thread_flag = True
        # self.update_thread.start()
        self.st_show_process = self._streamlit_process_start() # 启动可视化进程

    def _streamlit_process_start(self):
        script_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")  # streamlit 启动文件
        stream_lit_p = subprocess.Popen(["streamlit", "run", script_path])  # 启动 streamlit 可视化, 也需要定义数据格式
        self.log.info("streamlit_process start, pid is: ", stream_lit_p.pid) # 这个pid 打印不出来？
        return stream_lit_p

    def stop(self):
        # 关闭线程， 关闭可视化进程
        # self.update_thread_flag = False  # 更新数据线程结束
        # self.update_thread.join()
        self.log.info("update_thread stopped.")
        self.st_show_process.terminate() # 可视化进程等待结束
        self.log.info("st_show_process stopped.")

    def trade_data_update(self):
        # 使用文件读写的方式把数据传给 streamlit， 每次交易后调用, 修饰器update_after_trade_decorator
        self.fund_data_dict["current_time"] = int(time.time()) # 测试时间
        all_data_dict = {
            "stock_dict": self.stock_dict,
            "fund_data_dict": self.fund_data_dict
        }
        with json_data_lock:
            with open(IPC_FILE_ADDR, 'w') as f:
                json.dump(fp=f, obj=all_data_dict)

    @staticmethod
    def _check_fake_trader_input(code_name, num, value):
        # 由于是fake_trader 因此交易的时候需要同时提供 name， 数量， 金额，因此需要检查一下是否正确
        assert type(code_name) is str, "code_name need to be str type."
        assert len(code_name) == 6, "code_name must be six number len."

        if num is None or value is None:
            raise ValueError("Both num and value are necessary for fake_trader.")


    @update_after_trade_decorator
    def buy(self, code_name, num=None, value=None):
        # 买 num 个 name
        try:
            self._check_fake_trader_input(code_name, num, value)
            self.fund_data_dict["existing_fund"] -= num * value
            self.stock_dict[code_name] += num
        except:
            self.log.debug("something error occur at buy_fake_trader.")


    @update_after_trade_decorator
    def sell(self, code_name, num=None, value=None):
        # 卖 num 个 name
        try:
            self._check_fake_trader_input(code_name, num, value)
            if self.stock_dict[code_name] < num:
                self.log.debug("don't have enough number of stock:", code_name)
            self.fund_data_dict["existing_fund"] += num * value
            self.stock_dict[code_name] -= num
        except:
            self.log.debug("something error occur at sell_fake_trader.")


    @update_after_trade_decorator
    def sell_all(self):
        # 卖掉所有持仓
        raise NotImplementedError

    def check_position(self):
        # 查看股票持仓情况（持有情况）
        return self.stock_dict

    def check_cost_money(self):
        # 查看总共向账户投入的钱
        return self.fund_data_dict["existing_fund"]

    @update_after_trade_decorator
    def _add_money_to_account(self, money):
        # 继续向账户中投钱, 原则上只允许创建时调用
        self.fund_data_dict["initial_fund"] = money

    def get_today_deal(self):
        # 返回当日的所有交易
        raise NotImplementedError



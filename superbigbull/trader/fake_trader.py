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

json_data_lock = FileLock("data.json.lock", timeout=2) # 把数据写到json中 之前需要先拿到锁
"""
    但是由于我是在windows上写的代码，测试两个进程同时分别读写进程，也没有问题出现，在os似乎已经被加了锁
"""

BULL= {'BUY':0, "SELL":1} # 买卖方向

class OneDeal:
    # 一笔交易的类型， 时间，名字，数量，买卖方向
    def __init__(self, time, name, num, direction):
        pass

class FakeTrader:
    # 虚假的交易商， 会扣除你非常多的手续费
    def __init__(self, init_money=0, log=None):

        self.update_thread_flag = False # 数据提交线程控制位
        self.update_thread = threading.Thread(target=self.trade_data_update, name="Fake_Trader_update_thread")
        self.log = log
        self.st_show_process = None # 可视化进程 用于安全关闭

        self.stock_dict = dict() # 600519 : 持有数量
        self.fund_data_dict = {
            "initial_fund": 0,  # 投入资金
            "existing_fund": 0, #  现有资金
            "total_assets": 0, # 全部资产总和 = 现有资金 + 股票
            "current_time":0 # 当下的时间
        }

    def start(self):
        self.update_thread_flag = True
        self.update_thread.start()
        time.sleep(0.5) # 等待一会启动 可视化
        self.st_show_process = self._streamlit_process_start() # 启动可视化进程

    def _streamlit_process_start(self):
        script_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")  # streamlit 启动文件
        stream_lit_p = subprocess.Popen(["streamlit", "run", script_path])  # 启动 streamlit 可视化, 也需要定义数据格式
        self.log.info("streamlit_process start, pid is: ", stream_lit_p.pid)
        return stream_lit_p

    def stop(self):
        # 关闭线程， 关闭可视化进程
        self.update_thread_flag = False  # 更新数据线程结束
        self.update_thread.join()
        self.log.info("update_thread stopped.")
        self.st_show_process.terminate() # 可视化进程等待结束
        self.log.info("st_show_process stopped.")

    def trade_data_update(self):
        # 目前是使用最简答的文件读写的方式把数据传给 streamlit
        while self.update_thread_flag:
            # 启动一个线程，不断提交 交易数据到可视化进程， 可视化进程 负责web数据和 交易信息可视化

            self.fund_data_dict["current_time"] = int(time.time()) # 测试时间
            all_data_dict = {
                "stock_dict": self.stock_dict,
                "fund_data_dict": self.fund_data_dict
            }
            with json_data_lock:
                with open("data.json", 'w') as f:
                    json.dump(fp=f, obj=all_data_dict)

            time.sleep(1)

    def buy(self, name, num=None):
        # 买 num 个 name
        # 这里不会还要加锁吧， 最开始是串行处理吧， 可能真实一点的情况是，维护一个队列
        pass

    def sell(self, name, num=None):
        # 卖 num 个 name
        pass

    def sell_all(self):
        # 卖掉所有持仓
        pass

    def check_position(self):
        # 查看股票持仓情况（持有情况）
        pass

    def check_cost_money(self):
        # 查看总共向账户投入的钱
        pass

    def add_money_to_account(self):
        # 继续向账户中投钱
        pass

    def get_today_deal(self):
        # 返回当日的所有交易
        pass

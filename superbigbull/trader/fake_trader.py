"""
    这是一个假的 交易对象， 提供基本的买卖函数， 先越简单越好，

    然后的话， 应该是把数据引擎再次获取， 并且和交易信息全都可视化到网页端

"""
import multiprocessing
import threading
import subprocess
import time

from superbigshow.api import show_process, STOP_MSG

BULL= {'BUY':0, "SELL":1} # 买卖方向

class OneDeal:
    # 一笔交易的类型， 时间，名字，数量，买卖方向
    def __init__(self, time, name, num, direction):
        pass

class FakeTrader:
    # 虚假的交易商， 会扣除你非常多的手续费
    def __init__(self, init_money=0):
        # 初始资金
        # 这开一个子进程，包括数据获取 和 启动 streamlit
            # subprocess(streamlit)
        # 再开一个线程 提交更新， 不需要锁
        # threading(target=update)
        self.parent_conn, child_conn = multiprocessing.Pipe() # 创建管道， 返回两个端口
        self.show_process = multiprocessing.Process(target=show_process, name="Fake_Trader_show_p", args=(child_conn,)) # child_conn 传递给子进程

        self.update_thread_flag = False
        self.update_thread = threading.Thread(target=self.update, name="Fake_Trader_update_t")


    def start(self):
        self.show_process.start()
        self.update_thread_flag = True
        self.update_thread.start()


    def stop(self):
        self.show_process_send_stop() # 通知可视化进程结束
        time.sleep(1)
        self.show_process.join()# 等待结束
        print("show_process stopped.")

        self.update_thread_flag = False # 更新数据线程结束
        print("update_thread stopped.")

    def show_process_send_msg(self, msg):
        self.parent_conn.send(msg)

    def show_process_send_stop(self):
        self.parent_conn.send(STOP_MSG)

    def update(self):
        while self.update_thread_flag:
            # 启动一个线程，不断提交 交易数据到可视化进程， 可视化进程 负责web数据和 交易信息可视化
            time.sleep(1)
            self.show_process_send_msg([1,2,3,4])

    def buy(self, name, num=None):
        # 买 num 个 name
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



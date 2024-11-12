"""
    双均线策略， 就是一个短期均线， 一个长期均线， 来回交叉， 有的时候买入 有的时候卖出

    进而达到盈利
"""
from numexpr.expressions import max_int32

"""
    继承自 DefaultStrategy 的策略示例， 需要重载 init strategy log(可选) stop(选) 四个函数

    对事件引擎 handler 的注册， clock时钟引擎 handler 的注册，在main_engine中已经完成

    访问 main_engine 的成员 获取 事件和时钟、log引擎

    strategy 函数被策略基类的run 间接调用， run 中包了一层 错误处理
    
    均线策略：
     当前价格 大于 过去三个时刻的均价， 买入
     低于过去三个时刻的价格的均价，卖出
"""


from superbigcore.default_strategy import DefaultStrategy
from superbigcore.utils.superbiglog import DefaultLog
from superbigcore.push_engine.base_data_engine import BaseDataEngine
from superbigcore.main_engine import MainEngine
import superbigdata
from collections import deque

"""
这个数据类型的创建是为了配合 下面的 strategy_example， 没有其他用途
"""

PAST_WINDOW_LEN  = 3


class SmallDataEngine(BaseDataEngine):
    # 如果只是使用具体的几个股票数据，可以自定义数据引擎 ， 重载init和fetch函数
    EventType = "small_data_type"

    def __init__(self, event_engine, clock_engine, log):
        super().__init__(event_engine, clock_engine, log, push_interval=1)
        self.source = superbigdata.use('sina')

    def fetch_data(self):
        return self.source.stocks(['600519', '000001'])



class Strategy(DefaultStrategy):
    name = 'double_ma' # 策略的名字， main_engine 中加载时使用

    def __init__(self, main_engine:MainEngine):
        super().__init__(main_engine) # 有关的log_engine, 还有broker 都从main_engine 中进行获取
        self.main_engine = main_engine
        self.broker = self.main_engine.broker # 交易api

        self.stock_names = ['600519', '000001'] # 股票列表
        self.window_dict = {name: deque(maxlen=PAST_WINDOW_LEN) for name in self.stock_names} # deque 的字典

    def stop(self):
        # 把可视化进程杀掉
        self.log.info("double_ma_strategy closed.")

    def strategy(self, event):
        if event.event_type == 'small_data_type':
            for name, val in event.data.items(): # data 是一个字典
                print(name, 'current_price is: ', val['now'], "time is: ", val['time'])
                if name not in self.stock_names:
                    continue
                elif len(self.window_dict[name]) == PAST_WINDOW_LEN: #
                    if val['now'] > sum(self.window_dict[name]) / PAST_WINDOW_LEN:
                        self.broker.buy(name=name,val=val['now'], num=100)
                    else:
                        self.broker.sell_all()
                self.window_dict[name].append(val['now'])
        elif event.event_type == 'time_tick_type':
            print("处理时钟事件： ", event.event_type, event.clock_type)
            self.broker.sell_all()  #
        else:
            print("Undefined event_type", event.event_type)
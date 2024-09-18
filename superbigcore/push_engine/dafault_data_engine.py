"""
    默认的数据推送引擎，作用就是不断的获取数据，然后放入 Event_Engine 之中

    DefaultDataEngine 继承自 BaseDataEngine， 主要的 数据引擎启动，停止

    将获得的数据put 到Event_Engine 中等通用的功能函数，都被写在基类中，

    子类需要实现的只有具体的fetch_data() 函数 与 重载初始化函数

    因此当把 DefaultDataEngine 接入到 superbigdata 的数据爬取时，唯一用到的函数

    就是 superbigdata 的 all_market() , 返回所有 stock 的数据；

    获取具体特定的股票数据可以使用 stocks函数

"""
import time
import superbigdata
from .base_data_engine import BaseDataEngine

class DefaultDataEngine(BaseDataEngine):

    EventType = 'default_data_type' # 子类重载父类的事件类型

    def __init__(self, event_engine, clock_engine):
        super().__init__(event_engine, clock_engine) # 显示调用
        self.source = superbigdata.use('sina') # superbigdata 的接口


    def fetch_data(self):
        # 重载基类函数，每次返回数据
        return self.source.all_market()
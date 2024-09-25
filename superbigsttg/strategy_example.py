"""
    继承自 DefaultStrategy 的策略示例， 需要重载 init sttg log(可选) stop 四个函数

    对事件引擎 handler 的注册， clock时钟引擎 handler 的注册，都需要在策略中进行

    访问 main_engine 的成员 获取 事件和时钟引擎
"""


from superbigcore.default_strategy import DefaultStrategy
from superbigcore.utils.superbiglog import DefaultLog


class Strategy(DefaultStrategy):
    name = 'strategy_example' # 策略的名字
    def __init__(self, main_engine):
        super().__init__(main_engine)

    def strategy(self, event):
        pass

    def log_handler(self):
        # 这里如果不重载的话，返回的是main_engine 的log
        return DefaultLog(name='strategy_example',
                          log_type='file',
                          filepath='strategy_example.log',
                          loglevel='DEBUG')
    def stop(self):
        pass
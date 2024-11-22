"""
    默认的策略基类，使用时需要继承init函数， 选择继承log_handler

    具体的策略写在 strategy()里面，停止函数写在 stop中，

    run为外部调用接口，执行错误会向log中插入报错信息

"""


import sys
import traceback


class DefaultStrategy:

    name = "DefaultStrategy"
    def __init__(self, main_engine, name='example'):
        self.main_engine = main_engine
        # self.clock_engine = main_engine.clock_engine
        self.log = self.log_handler() or self.main_engine.log # 返回一个log
        self.name = name # 策略的名字用于区分不同的策略

    def log_handler(self):
        return None

    def strategy(self, event):
        # 具体的策略执行函数
        pass

    def run(self, event):
        try:
            self.strategy(event) # 调用策略函数
        except: #
            exc_type, exc_value, exc_traceback = sys.exc_info() # 返回报错信息
            # Traceback objects represent the stack trace of an exception. A traceback object is implicitly created
            # when an exception occurs, and may also be explicitly created by calling types.TracebackType.
            self.log.error(traceback.format_exception( # 这里把tb对象解析，并做了一个格式化的输出
                exc_type,
                exc_value,
                exc_traceback
            ))

    def stop(self):
        pass


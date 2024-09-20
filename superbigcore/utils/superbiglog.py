"""
    添加 log的帮助函数，打印日志，这里使用的时logbook，也可使用logging 进行替换

    logbook:

    > So how are handlers registered? If you are used to the standard Python logging system,
    it works a little bit differently here. Handlers can be registered for a thread or for a
    whole process or individually for a logger. However, it is strongly recommended not to
    add handlers to loggers unless there is a very good use case for that.



"""
import os
import sys
import logbook
import logging # 有机会可以使用 logging 进行对logbook 的替换
from logbook import Logger, StreamHandler, FileHandler


class DefaultLog:

    def __init__(self, name='default', log_type='stdout', filepath='default.log', loglevel='DEBUG'):
        self.log = Logger(name)

        if log_type == "stdout":
            StreamHandler(sys.stdout, level=loglevel).push_application() # push_application 全部注册

        elif log_type == "file":
            if not os.path.exists(filepath):
                os.makedirs(filepath) # 递归创建
            file_handler = FileHandler(filepath, level=loglevel) #
            self.log.handlers.append(file_handler) # 只给 log 注册 handler

    # def __getattr__(self, item, *args, **kwargs):
    #     # 如果找不到参数item， 调用__getattr__
    #     # 访问对象的所有元素都会调用 __getattribute__
    #     return self.log.__getattribute__(item, *args, **kwargs) # 可变参数
    #     # 这里不理解

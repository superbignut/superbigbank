"""




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
            StreamHandler(sys.stdout, level=loglevel).push_application() # push_application 与 handlers的方式都可以

        elif log_type == "file":
            if not os.path.exists(filepath):
                os.makedirs(filepath) # 递归创建
            file_handler = FileHandler(filepath, level=loglevel) # push_application 应该也可以
            self.log.handlers.append(file_handler)

    def __getattr__(self, item, *args, **kwargs):
        # 如果找不到参数item， 调用__getattr__
        # 访问对象的所有元素都会调用 __getattribute__
        return self.log.__getattribute__(item, *args, **kwargs) # 可变参数

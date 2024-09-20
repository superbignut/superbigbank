import multiprocessing
import os
import threading
import time
from collections import defaultdict, deque
import datetime
import arrow

class A(object):
    aaa = 1
    def fun(self):
        print(self.aaa)

class C(A):
    aaa = 3
    def __init__(self):
        print(self.aaa)



class B(A):
    bbb = 1
    def __getattr__(self, item):
        print("yes1")
    def __getattribute__(self, item):
        print("yes2")
        return object.__getattribute__(self, item)


if __name__ == '__main__':
    c = C()
    c.fun()













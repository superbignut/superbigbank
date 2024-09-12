import multiprocessing
import os
import threading
import time
from collections import defaultdict, deque
import datetime
import arrow

class A:
    def __init__(self):
        self.aaa = 1
        self.bbb =  1 if self.aaa <= 1 else 2


if __name__ == '__main__':
    a = datetime.datetime.now().date()
    b = arrow.get(time.time())

    print(type(a))
    print(b)












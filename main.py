import multiprocessing
import os
import threading
import time
from collections import defaultdict, deque
import datetime
import arrow

class A:

    def __init__(self):
        self.aaa = 2

class B(A):
    bbb = 1
    def __getattr__(self, item):
        print("yes1")

    def __getattribute__(self, item):
        print("yes2")
        return object.__getattribute__(self, item)

if __name__ == '__main__':
    b = B()
    print(b.bbbc)












import multiprocessing
import os
import signal
import threading
import time
from collections import defaultdict, deque
import datetime
from collections import OrderedDict
from socket import has_dualstack_ipv6

import arrow
import dash
import sys

import signal


def signal_handler(signal_number, stack_frame):
    # self.stop() # 结束子线程 # Todo 这个stop函数需要进一步完善
    # self.log.info("yes")
    # print("yes111")
    sys.exit()  # 结束主线程

if __name__ == '__main__':
    signal.signal(signalnum=signal.SIGINT, handler=signal_handler)

    while True:
        print(threading.active_count())
        pass















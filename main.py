import multiprocessing
import os
import threading
import time
from collections import defaultdict

d = defaultdict(list)

if __name__ == '__main__':
    item = 2
    if 100 not in d[item]:
        pass
        # d[item].append(100)
    print(3 in d)
    print(d)
    d.pop(2)
    print(d.get(2))













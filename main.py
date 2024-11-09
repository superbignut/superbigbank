import multiprocessing
import os
import json
import time

from filelock import  FileLock

temp_lock = FileLock("clock_test.py", timeout=2) # 把数据写到json中 之前需要先拿到锁

if __name__ == '__main__':
    while True:
        with temp_lock:
            with open("snowball.json", "w") as f:
                json.dump(fp=f, obj={
                    "time":time.time()
                })
        time.sleep(0.5)


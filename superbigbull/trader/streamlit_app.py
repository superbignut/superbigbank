"""
    通过读取中间文件data.json 进而使用streamlit 来在网页端可视化数据，

    读取前，为保证安全，需要先对文件上锁，使用的是 filelock包
"""
import multiprocessing
import threading
import time
import json
from filelock import FileLock
import streamlit as st

json_data_lock = FileLock("data.json.lock", timeout=2) # 把数据写到json中 之前需要先拿到锁

# 定义一个函数读取 JSON 文件
def _load_json_data():
    with json_data_lock:
        with open("data.json", "r") as f:
            return json.load(f)


if __name__ == "__main__":
    data_placeholder = st.empty()
    while True:
        data = _load_json_data()
        data_placeholder.json(data)  # 或者使用 st.write(data)
        time.sleep(2)

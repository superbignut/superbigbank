
import os
import sys
import time
import subprocess
import signal

STOP_MSG = "stop_msg"

def show_process(conn):
    # 启动子进程， 包括数据的可视化和交易信息的可视化
    print("show_process pid is: ", os.getpid())

    script_path = os.path.join(os.path.dirname(__file__), "app.py") # streamlit 启动文件
    stream_lit_p = subprocess.Popen(["streamlit", "run", script_path]) # 启动 streamlit 可视化
    print("streamlit pid is: ", stream_lit_p.pid)

    while True:
        temp_data = conn.recv() # 接收管道的数据
        if temp_data == STOP_MSG:
            os.kill(stream_lit_p.pid, signal.SIGINT) # 杀掉 streamlit 进程
            sys.exit() # 退出本进程
        else:
            print(temp_data)
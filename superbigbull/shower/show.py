"""




"""
import os
import sys
import time
import subprocess
import signal

STOP_MSG = "stop_msg"

# active_flag = True

# def signal_handler(signal_number, stack_frame):


def show_process(conn):
    # 可视化进程， 包括数据的可视化和交易信息的可视化
    print("show_process pid is: ", os.getpid())

    script_path = os.path.join(os.path.dirname(__file__), "app.py") # streamlit 启动文件
    stream_lit_p = subprocess.Popen(["streamlit", "run", script_path]) # 启动 streamlit 可视化, 也需要定义数据格式
    print("streamlit pid is: ", stream_lit_p.pid)


    while True:
        try:
            temp_data = conn.recv() # 接收管道的数据 # 这里的数据格式需要定义一下
        except KeyboardInterrupt: # 关闭进程时会触发
            sys.exit()

        if temp_data == STOP_MSG:
            os.kill(stream_lit_p.pid, signal.SIGINT) # 杀掉 streamlit 进程
            sys.exit() # 退出本进程
        else:
            print(temp_data)
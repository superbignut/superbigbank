"""




"""
import os
import sys
import time
import subprocess
import signal



# STOP_MSG = "stop_msg"
def signal_handler(signal_number, stack_frame):
    # 这里最好能等待 streamlit 进程结束
    # time.sleep(2)  # 子进程慢点关闭
    print("sigint_signal is captured by show_process.") # 这里需要等待接受完毕之后 在关闭，否则管道报错

    raise ValueError # 这里可以自定义错误类型



class DefaultShower:
    def __init__(self, data_engine, log):
        pass


def show_process(conn):
    signal.signal(signal.SIGINT, handler=signal_handler)  # 注册 ctrl + c 信号处理函数
    # 可视化进程， 包括数据的可视化和交易信息的可视化
    print("show_process pid is: ", os.getpid())

    script_path = os.path.join(os.path.dirname(__file__), "app.py") # streamlit 启动文件
    stream_lit_p = subprocess.Popen(["streamlit", "run", script_path]) # 启动 streamlit 可视化, 也需要定义数据格式
    print("streamlit pid is: ", stream_lit_p.pid)
    while True:

        try:
            temp_data = conn.recv()  # 接收管道的数据 # 这里的数据格式需要定义一下
            print(temp_data)
        except ValueError: # ctrl+c 关闭进程时会触发,
            conn.close() # 关闭 conn
            stream_lit_p.terminate() # 关闭子进程 streamlit
            sys.exit() # 安全退出

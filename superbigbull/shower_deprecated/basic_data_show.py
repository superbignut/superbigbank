"""
    由于我使用的是recv 阻塞的接受数据的函数， 因此当我使用ctrl+c 中断程序执行的时候，

    大概率报错 是InterruptedError， 因此 这个进程的中断 原因 并不是 发送通道端口的关闭

    虽然，发送端口确实也被关闭了，但是时间已经在ctrl+c之后了

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

    # raise ValueError # 这里可以自定义错误类型



class DefaultShower:
    def __init__(self, data_engine, log):
        pass


def show_process(conn):
    signal.signal(signal.SIGINT, handler=signal_handler)  # 注册 ctrl + c 信号处理函数， 但没什么用
    # 可视化进程， 包括数据的可视化和交易信息的可视化
    print("show_process pid is: ", os.getpid())

    script_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py") # streamlit 启动文件
    stream_lit_p = subprocess.Popen(["streamlit", "run", script_path]) # 启动 streamlit 可视化, 也需要定义数据格式
    print("streamlit pid is: ", stream_lit_p.pid)
    while True:

        try:
            stock_list, stock_dict, initial_fund, existing_fund, total_assets = conn.recv()  #  报错 中断函数调用， 改成poll 会好吗
            print(initial_fund)

        except (InterruptedError, EOFError) as e: # ctrl+c 关闭进程时会触发
            print("show_process is closed by except InterruptedError or EOF_ERROR:", e)
            stream_lit_p.terminate() # 关闭子进程 streamlit
            print("stream_lit_p is closed by show_process normally.")
            sys.exit() # 安全退出


if __name__ == "__main__":
    p = subprocess.Popen(["streamlit", "run", "./streamlit_app.py"])
    while True:
        time.sleep(1)

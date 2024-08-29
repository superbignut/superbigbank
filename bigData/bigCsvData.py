from bigCore import DataHandler, MarketEvent
from queue import Queue # 线程安全的队列
import pandas as pd
import os
import time
import threading

class CsvDataHandler(DataHandler):
    """读取csv的数据类型，需要实现基类的纯虚函数"""
    def __init__(self, event_queue, file_name, duration=1):

        def __parse_csv_file(file_name_):
            df = pd.read_csv(file_name)
            df['symbol'] = os.path.basename(file_name).strip('.csv')
            df.reset_index(inplace=True, drop=True) # 删除已有index
            return df

        self._data = __parse_csv_file(file_name_=file_name) # 读取数据
        self._cursor = 0                       # 读取csv数据的全局 index
        self._duration= duration
        self._event_queue = event_queue       # 全局事件队列
        # print(self._data[0:10])

    def run(self):
        """执行，开始不断读取数据"""
        def __run():
            while self._cursor < len(self._data):
                self._event_queue.put(MarketEvent()) # 把一个数据对象放到queue 中,因为这是csv 所以暂时没有处理
                self._cursor += 1
                print("\n#### Market Simulation Generation ###", time.ctime(time.time())[11:-5])
                time.sleep(self._duration) # sleep 一段时间

        temp_thread = threading.Thread(target=__run) # 传递调用对象
        temp_thread.start() # 启动线程


    def get_current_bar(self):
        """Get the Current data at self._cursor"""
        return self._data.iloc[self._cursor]


    def get_pre_bars(self, n=1):
        """Get the Current data at self._cursor - 1"""
        return self._data.iloc[self._cursor - n : self._cursor]



if __name__ == '__main__':
    q = Queue()
    a = CsvDataHandler(event_queue=q, file_name='../local_data/IF.csv', duration=1)
    a.run()

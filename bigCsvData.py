from bigCore import DataHandler
from queue import Queue
import pandas as pd

class CsvDataHandler(DataHandler):
    """
    读取csv的数据类型，需要实现基类的纯虚函数
    """
    def __init__(self, event_queue_, file_name_, speed_=1):

        def __parse_csv_file(file_name):
            df = pd.read_csv(file_name)
            print(len(df),type(df))
            print(df.iloc[0])

        __parse_csv_file(file_name=file_name_)
        self._cursor = 0                      # 读取csv数据的全局 index
        self._event_queue = event_queue_      # 全局事件队列


        pass

    def run(self):
        def __run():
            pass
        pass

    def get_current_bar(self):
        pass

    def get_pre_bars(self):
        pass


if __name__ == '__main__':
    q = Queue()
    CsvDataHandler(event_queue_=q, file_name_='local_data/IF.csv', speed_=1)


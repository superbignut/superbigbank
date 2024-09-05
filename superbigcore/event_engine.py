import time
from collections import defaultdict
from queue import Queue, Empty
import threading



class Event:

    def __init__(self, event_type):
        pass
        # self.event_type = event_type



class EventEngine:

    def __init__(self):

        self.__queue = Queue() # 事件队列

        self.__active = False # 启动开关

        self.__thread = threading.Thread(target=self.__run, name="EventEngine.__thread") # 包含主函数的线程

        self.__handlers = defaultdict(list) # 事件处理函数字典，同一个事件可以有多个处理函数 event.event_type : func()


    def __run(self):
        # 从队列中取出事件，并启动相应的线程
        while self.__active:
            try:
                event = self.__queue.get(block=True, timeout=1) # 阻塞和等待时间
                handle_thread = threading.Thread(target=self.__process,name="EventEngine.__process", args=(event,)) # 名字相同但没关系
                handle_thread.start()
            except Empty:
                pass

    def __process(self, event):
        # 从字典中取出处理函数，进行对事件的处理
        if event.event_type in self.__handlers:
            for handler in self.__handlers[event.event_type]:
                handler(event)

    def start(self):
        # 启动轮询主线程
        self.__active = True
        self.__thread.start()

    def stop(self):
        # 关闭轮询主线程
        self.__active = False
        self.__thread.join() # 这里

    def register(self, event_type, handler):
        # 注册 事件类型对应的处理函数
        if handler not in self.__handlers[event_type]: # []访问失败会创建空list
            self.__handlers[event_type].append(handler)

    def unregister(self, event_type, handler):
        # 注销 事件类型对应的处理函数
        handler_list = self.__handlers.get(event_type) # get 不会触发 defaultdict
        if handler_list is None:
            return
        if handler in handler_list:
            handler_list.remove(handler)
            if len(handler_list) == 0:
                self.__handlers.pop(event_type)


    def put(self, event):
        # 封装向 __queue中加入元素
        self.__queue.put(event)

    @property
    def queue_size(self):
        # 封装size
        return self.__queue.qsize()



if __name__ == '__main__':
    a = EventEngine()
    a.start()
    time.sleep(5)
    a.stop()
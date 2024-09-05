"""

    作为事件驱动引擎的 被处理单位，事件可以有很多种，可以有 比如 Market_Event, Order_Event 等

    这些事件在生成时被 put到 queue 中， 被 get 后由相应的处理函数处理， 如果有新的 Event产生则又

    会进行同样的操作；

    但如果简单的事件只有 type和 data两个变量，则统一用 Event 进行封装， 使用 event_type 进行区分

    不同的事件，具体的数据则 放在data 中；


"""

class Event:
    def __init__(self, event_type, data):
        # 简单的构造函数，赋值两个成员变量
        self.event_type = event_type
        self.data = data


    # self.event_type:
    #  + default_data_type 默认的数据产生事件
    #  +
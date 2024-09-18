"""
    向 event_engine 中推送事件的 推送引擎, push_engine:

     目前包括了基本的数据数据引擎 base_data_engine, 其他的自定义的数据推送引擎可以直接继承

    default_data_engine 则是 一个继承实例， 每次获取交易所全部股票数据

    clock_data_engine 为时钟引擎，每次向 event_engine中推送 时间事件，可以是间隔时间事件，也可以是

    固定时刻的时间事件，
"""

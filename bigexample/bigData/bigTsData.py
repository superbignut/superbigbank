# 这里应该是对各种数据接口或者自己的爬虫接口的统一封装
# baostock 似乎也可以获取数据

import tushare as ts

class TsDataHandler:
    def __init__(self):
        """
        tushare 数据的初始化
        """
        # 数据来自于tushare
        self._data_interface_name = "tushare"

        # 设置 tushare token，只需要设置一次
        ts.set_token("59a67ba5d9a41cb47c3e0fb72b7d4b778d4e69766b27d91ad9b7b2df")

        # tushare 接口初始化, 进而可以调用pro_api下的一些函数，但是目前只用ts的通用行情接口，这个暂未使用
        # self._data_pro_api = ts.pro_api()
        # self._data_pro_api.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718') 是未复权的数据

    @staticmethod
    def get_oneday_data(self):
        pass

    @staticmethod
    def get_duration_data(code_name_='000001.SZ',adj_='qfq', start_date_='20180101', end_date_='20190101'):
        """
        获取一个区间的股票数据
        :param code_name_: 股票代码
        :param adj_: 是否复权
        :param start_date_: 开始时间
        :param end_date_: 结束时间
        :return: 返回数据
        """
        # ts.pro_bar 调用tushare 的通用的行情接口 https://tushare.pro/document/2?doc_id=109 可以获得更全面的数据
        # 检测可以以后写成通用函数
        temp_data_frame = ts.pro_bar(ts_code=code_name_, adj=adj_, start_date=start_date_, end_date=end_date_)

        return temp_data_frame

    @staticmethod
    def get_recent_data(code_name_='000001.SZ', src_='sina'):
        """
        获取一个具体日期的股票数据, 具体来自ts 的爬虫接口
        :param code_name_:
        :param src_:
        :return: <class 'pandas.core.frame.DataFrame'> .iloc[0] dim = 32
        """
        # ts 可以从 sina 和dc 两个网站进行爬虫 获得实时数据
        temp_recent_data = ts.realtime_quote(ts_code=code_name_, src=src_)

        return temp_recent_data.iloc[0]

"""
0    NAME       str     股票名称           
1    TS_CODE    str     股票代码           
2    DATE       str     交易日期           
3    TIME       str     交易时间           
4    OPEN       float   开盘价            
5    PRE_CLOSE  float   昨收价            
6    PRICE      float   现价             
7    HIGH       float   今日最高价          
8    LOW        float   今日最低价          
9    BID        float   竞买价，即“买一”报价（元） 
10   ASK        float   竞卖价，即“卖一”报价（元） 
11   VOLUME     int     成交量（src=sina时是股，src=dc时是手）
12   AMOUNT     float   成交金额（元         
13   B1_V       float   委买一（量，单位：手，下同） 
14   B1_P       float   委买一（价，单位：元，下同） 
15   B2_V       float   委买二（量）         
16   B2_P       float   委买二（价）         
17   B3_V       float   委买三（量）         
18   B3_P       float   委买三（价）         
19   B4_V       float   委买四（量）         
20   B4_P       float   委买四（价）         
21   B5_V       float   委买五（量）         
22   B5_P       float   委买五（价）         
23   A1_V       float   委卖一（量，单位：手，下同） 
24   A1_P       float   委卖一（价，单位：元，下同） 
25   A2_V       float   委卖二（量）         
26   A2_P       float   委卖二（价）         
27   A3_V       float   委卖三（量）         
28   A3_P       float   委卖三（价）         
29   A4_V       float   委卖四（量）         
30   A4_P       float   委卖四（价）         
31   A5_V       float   委卖五（量）         
32   A5_P       float   委卖五（价）                  
"""

if __name__ == '__main__':
    _data = TsDataHandler()
    print(_data.get_recent_data())

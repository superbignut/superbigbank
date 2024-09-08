"""
    sina 的数据子类的实现，处于某种原因，需要实现进一步的_get_headers（）

    此外，stock_api 和 _format_response_data 则是子类的虚函数实现
"""


# headers={'Referer' :'https://finance.sina.com.cn'}
# url='https://hq.sinajs.cn/list=sh600519'
# file=requests.get(url=url,headers=headers)
# print(file.text)

import re
import time

from tushare import stock_issuance

from .basedata import BaseData # 相对位置的引入会导致无法运行本地 __main__

class Sina(BaseData):

    # var hq_str_sh999991="";
    sina_null_data_re_pattern = re.compile(
        r"(\w{2}\d+)=\"\";"
    )
    """
        var hq_str_sh600519="贵州茅台,1430.000,1443.190,1395.000,1438.000,1395.000,1395.000,1395.170,3413459,4801049927.000,
        5760,1395.000,200,1394.990,100,1394.980,100,1394.900,100,1394.890,200,1395.170,300,1395.190,400,1395.200,400,1395.240,1850,1395.250,2024-09-02,15:00:00,00,";
    """
    sina_stock_data_re_pattern = re.compile(
        r"(\w{2}\d+)=\S([^\s,]+?)%s%s"
        % (r",([\.\d]+)" * 29,  r",([-\.\d:]+)" * 2)
    )
    def __init__(self):
        super().__init__()

    @property
    def stock_api(self) -> str:
        # sina 的 接口 api
        return f"https://hq.sinajs.cn/rn={int(time.time() * 1000)}&list="

    def _get_headers(self) -> dict:
        # sina 需要增加header 否则被forbidden
        headers = super()._get_headers()
        return {
            **headers,
            'Referer': 'https://finance.sina.com.cn/'
        }

    def _format_response_data(self, data:list[str])->dict:
        # 格式话从web 上返回的数据
        stocks_all = ''.join(data)
        stocks_all = self.sina_null_data_re_pattern.sub("", stocks_all) # 去掉获取失败的情况
        result = self.sina_stock_data_re_pattern.finditer(stocks_all) # 对有效字符进行匹配,返回迭代器
        stock_dict = dict()
        for item in result:
            stock_info = item.groups() # 所有的捕获内容 1 + 1 + 29 + 2
            stock_dict[stock_info[0]] = dict(
                name=stock_info[1],
                open=float(stock_info[2]),
                close=float(stock_info[3]),
                now=float(stock_info[4]),
                high=float(stock_info[5]),
                low=float(stock_info[6]),
                buy=float(stock_info[7]),
                sell=float(stock_info[8]),
                turnover=int(stock_info[9]),
                volume=float(stock_info[10]),
                bid1_volume=int(stock_info[11]),
                bid1=float(stock_info[12]),
                bid2_volume=int(stock_info[13]),
                bid2=float(stock_info[14]),
                bid3_volume=int(stock_info[15]),
                bid3=float(stock_info[16]),
                bid4_volume=int(stock_info[17]),
                bid4=float(stock_info[18]),
                bid5_volume=int(stock_info[19]),
                bid5=float(stock_info[20]),
                ask1_volume=int(stock_info[21]),
                ask1=float(stock_info[22]),
                ask2_volume=int(stock_info[23]),
                ask2=float(stock_info[24]),
                ask3_volume=int(stock_info[25]),
                ask3=float(stock_info[26]),
                ask4_volume=int(stock_info[27]),
                ask4=float(stock_info[28]),
                ask5_volume=int(stock_info[29]),
                ask5=float(stock_info[30]),
                date=stock_info[31],
                time=stock_info[32],
            )

        return stock_dict

if __name__ == '__main__':
    sina = Sina()
    s1 = sina.stocks(['600519','999991','000001','600619'])
    print(s1)

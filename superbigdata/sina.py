# headers={'Referer' :'https://finance.sina.com.cn'}
# url='https://hq.sinajs.cn/list=sh600519'
# file=requests.get(url=url,headers=headers)
# print(file.text)

import re
import time
from . import basedata

class Sina(basedata.BaseData):
    
    def __init__(self):
        super().__init__()

    
    @property
    def stock_api(self) -> str:
        pass
    pass

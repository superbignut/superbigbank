import os
import re
import requests
import json

# 股票代码的存储地址
STOCK_CODE_PATH = os.path.join(os.path.dirname(__file__), 'stock_code.conf')

def update_stock_codes()->list:
    # 读取出 http://www.shdjt.com/js/lib/astock.js 中的所有股票代码并写入conf 文件
    response = requests.get("http://www.shdjt.com/js/lib/astock.js")
    if response.status_code != 200:
        raise RuntimeError
    stock_codes = re.findall(r'~([0-9a-z]*)`', response.text)
    # 这里其实可以把中文名字一起读出来 Todo
    with open(STOCK_CODE_PATH,'w', encoding='utf8') as temp_f:
        temp_f.write(json.dumps({"stock": stock_codes}))
    return stock_codes

def get_stock_codes(realtime=False)->list:
    # 读取存储的股票代码 realtime 表示是否在读取前更新数据
    if realtime:
        return update_stock_codes()
    else:
        with open(STOCK_CODE_PATH, 'r', encoding='utf8') as temp_f:
            temp_str = temp_f.read()
            return json.loads(temp_str)['stock']

def get_stock_type(stock_code:str)->str:
    # 返回股票代码属于那个交易所
    # ['50', '51', '60', '90', '110','113','118','132','204','5', '6','7','9'] 为 sh
    # ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    assert type(stock_code) is str, "stock code need to be str type."
    sh_head = ('50','51','60','90','110','113','118','132','204','5','6','7','9')
    if stock_code.startswith(('sh','sz','zz')):
        return stock_code[:2]
    else:
        return 'sh' if stock_code.startswith(sh_head) else 'sz'

def get_stock_list_with_type_prefix(stock_codes:list):
    # 输入股票代号列表，返回带交易所的股票代码列表
    return [get_stock_with_type_prefix(stock_code) for stock_code in stock_codes]

def get_stock_with_type_prefix(stock_code:str)->str:
    # 给股票代码号加上前缀
    return get_stock_type(stock_code) + stock_code[-6:]

if __name__ == '__main__':
    print(get_stock_list_with_type_prefix(['600519', 'sz000001']))











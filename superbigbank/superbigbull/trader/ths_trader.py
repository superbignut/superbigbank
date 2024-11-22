"""
    这个交易方式为使用 ths_trader 在安卓模拟器上THS-APP 模拟点击来进行模拟交易的trader

    参考 https://github.com/nladuo/THSTrader

    核心包为 uiautomator2， easyocr 来模拟操作和进行文字识别， 但总感觉速度较慢

"""

import time
from datetime import datetime
import uiautomator2 as u2
import easyocr
from PIL import Image
import numpy as np
# resource-id、分布关系和各种信息 可以在手机端使用 autox.js查看


"""
交易的xml
<node index="3" text="" resource-id="" class="android.widget.RelativeLayout" package="com.hexin.plat.android" content-desc="交易"

  <node index="0" text="" resource-id="com.hexin.plat.android:id/icon" class="android.widget.ImageView" package="com.hexin.plat.android" content-desc="" 

  <node index="1" text="交易" resource-id="com.hexin.plat.android:id/title" class="android.widget.TextView" package="com.hexin.plat.android" content-desc="" 

</node>
"""


# 比较通用的资源id， 私有的只放在具体的函数中
RESOURCE_ID_DICT = {
    "mo_ni_button" : 'com.hexin.plat.android:id/tab_mn', # 交易tab下的 "模拟" 按键
    "close_button" : "com.hexin.plat.android:id/close_button", # 申购弹窗右上角有个叉
    "ok_button" : "com.hexin.plat.android:id/ok_btn", # 偶尔会弹出开的，需要点 "确定" 才能退出
    "title_bar_img" : "com.hexin.plat.android:id/title_bar_img", # 交易界面，持仓等按钮点进去的左上角的 "<" logo
    "stockname_tv": "com.hexin.plat.android:id/stockname_tv", # 输入代号后，需要手动确定的情况 000006
}

THS_PACKAGE_NAME = "com.hexin.plat.android"

MAX_GET_POSITION = 20

class THSTrader:
    def __init__(self, serial="emulator-5554"):
        self.d = u2.connect_usb(serial=serial)  # 模拟器
        self.reader = easyocr.Reader(lang_list=['ch_sim', 'en']) # 识别器
        self.__open_app_goto_moni_page() # 切进去
        print("THS_Trader init finished.")


    def buy(self, stock_code:str, count:int, price:float):
        # 模拟买入
        if self.__buy_and_sell_actions(stock_code=stock_code, count=count, price=price, bull_flag="menu_buy_image"):
            print("buy successfully!")
        else:
            print("buy failed!")

    def sell(self, stock_code:str, count:int, price:float):
        # 模拟卖出
        if self.__buy_and_sell_actions(stock_code=stock_code, count=count, price=price, bull_flag="menu_sale_image"):
            print("sell successfully!")
        else:
            print("sell failed!")


    def get_balance(self):
        # 获取持仓界面总信息
        self.__util_close_others() # 清空
        #########################
        self.d(resourceId="com.hexin.plat.android:id/menu_holdings_image").click()
        temp_return = {
            "total_asset_value": float(
                self.d(resourceId="com.hexin.plat.android:id/totalasset_value").get_text().replace(",", "")),
            "can_use_value": float(
                self.d(resourceId="com.hexin.plat.android:id/canuse_value").get_text().replace(",", "")),
            "total_worth_value": float(
                self.d(resourceId="com.hexin.plat.android:id/totalworth_value").get_text().replace(",", "")),
        }
        ########################## 回到初始界面
        self.__back_to_moni_page()
        ##########################
        return temp_return


    def get_position(self):
        # 返回所有的stock的 名字， 持仓数量， 可用数量， 建议初始化时使用，模仿点击与滑动，存在一定延迟
        self.__util_close_others()  # 清空
        #########################
        self.d(resourceId="com.hexin.plat.android:id/menu_holdings_image").click()
        i = 0
        while i < MAX_GET_POSITION:
            try:
                (self.d
                .xpath(f'//*[@resource-id="com.hexin.plat.android:id/recyclerview_id"]')
                .child(f"/android.widget.RelativeLayout[{i+1}]")
                .get(timeout=0.5)
                .screenshot()
                .save(f"tmp_png/tmp{i}.png"))
                i += 1
                self.d.swipe(340, 1000, 340, 880)
            except:
                break
        _count = i
        # print(_count)
        _holdings = []
        for i in range(_count):
            # print(i)
            _holdings.append(self.__ocr_parse_holding(f"tmp_png/tmp{i}.png"))

        ########################## 回到初始界面
        self.__back_to_moni_page()
        ##########################
        return _holdings

    def __buy_and_sell_actions(self, stock_code:str, count:int, price:float, bull_flag:str):
        # 整合买卖股票的具体点击行为, 返回True 也有可能没有交易成功
        self.__util_close_others()  # 清空
        #########################
        return_f = True
        try:
            assert bull_flag == "menu_buy_image" or bull_flag == "menu_sale_image", "bull_flag error."
            assert type(stock_code) is str, "stock_code must be a str."
            assert type(count) is int and type(price) is float, "amount or price type error."

            self.d(resourceId=f"com.hexin.plat.android:id/{bull_flag}").click()
            self.__input_stock_code(stock_code)
            self.__input_stock_count(count)
            self.__input_stock_price(price)

            self.d(resourceId="com.hexin.plat.android:id/transaction_layout").click() # 模拟买入
            if self.__bull_double_check(stock_code, count, price):
                self.d(resourceId="com.hexin.plat.android:id/ok_btn").click() # bull前确定
                time.sleep(1)

                if self.__check_insufficient_account(): # 查看是否提示账户余额不足
                    return_f = False

                self.d(resourceId="com.hexin.plat.android:id/ok_btn").click() # bull后确定
            else:
                self.d(resourceId="com.hexin.plat.android:id/cancel_btn").click() # 有输入错误的情况，点取消
                print("double_check error.")
        except:
            return_f = False
        finally:
            time.sleep(1) # 这里交易之后会刷一下，所以要sleep
            #########################
            self.__back_to_moni_page()
            #########################
            return return_f

    def __bull_double_check(self, stock_code:str, count:int, price:float):
        # 确认买入之前的再次检查
        if self.d(resourceId="com.hexin.plat.android:id/stock_code_value").get_text().replace(" ", "") != stock_code:
            return False
        if self.d(resourceId="com.hexin.plat.android:id/number_value").get_text().replace(" ", "").replace(",", "") != str(count):
            return False
        price = float(price)
        _temp_price = float(self.d(resourceId="com.hexin.plat.android:id/price_value").get_text())
        if abs(price - _temp_price) > 0.01:
            return False
        return True


    def __input_stock_code(self, stock_code):
        # 输入stock code : 600519
        self.__util_close_others()  # 清空
        #########################
        self.d(resourceId="com.hexin.plat.android:id/content_stock").click()
        self.__util_input_text(text=stock_code)
        time.sleep(1) # 输入后等待刷新
        if self.__util_check_id_in_app_page(RESOURCE_ID_DICT["stockname_tv"]):
            try:
                self.d.xpath('//*[@resource-id="com.hexin.plat.android:id/recyclerView"]').child('/android.widget.RelativeLayout[1]').click()
            except:
                pass

    def __input_stock_count(self, count):
        # 输入数量
        self.__util_close_others()
        self.d(resourceId="com.hexin.plat.android:id/stockvolume").click()
        self.__util_input_text(count)

    def __input_stock_price(self, price):
        # 输入价格
        self.__util_close_others()  # 清空
        self.d(resourceId="com.hexin.plat.android:id/stockprice").click()
        self.__util_input_text(text=price)

    def __util_input_text(self, text):
        # 输入文字
        self.d.shell("input keyevent 123") # 光标移动到最后
        for _ in range(20):
            self.d.shell("input keyevent 67") # 删除已有内容
        self.d.shell(f"input text {text}")


    def __check_insufficient_account(self):
        # 检查点击交易 是否弹出 交易失败的信息
        _tmp_png = np.array(self.d(resourceId="com.hexin.plat.android:id/content_scroll").screenshot())
        _pop_text = self.reader.readtext(_tmp_png)[0][1]
        if "不足" in _pop_text:
            print("股票余额不足")
            return True
        if "不允许" in _pop_text:
            print("股票余额不足")
            return True
        if "请稍后" in _pop_text:
            print("交易失败")
            return True
        return False

    def __ocr_parse_holding(self, path):
        # 使用ocr 识别 持仓的名字， 持仓数量， 可用数量,
        # 但是在实际使用中似乎没必要通过这个查， 初始化的时候查一下还ok
        _tmp_png = np.array(Image.open(path).crop((11, 11, 165, 55)))
        _stock_name = self.reader.readtext(_tmp_png)[0][1]

        _tmp_png = np.array(Image.open(path).crop((419, 11, 548, 55)))
        try:
            _stock_count = self.reader.readtext(_tmp_png)[0][1]
        except IndexError:  # _stock_count是0时候reader返回的是空列表
            _stock_count = "0"

        _tmp_png = np.array(Image.open(path).crop((419, 60, 548, 102)))
        try:
            _stock_available = self.reader.readtext(_tmp_png)[0][1]
        except IndexError: # _stock_available是0时候reader返回的是空列表
            _stock_available = "0"
        return {
            "stock_name": _stock_name.replace(" ", ""),
            "stock_count": int(_stock_count.replace(",", "")),
            "stock_available_num": int(_stock_available.replace(",", ""))
        }


    def __back_to_moni_page(self):
        # 切回到最初的模拟炒股界面
        self.__util_close_others()
        if self.__util_check_id_in_app_page(RESOURCE_ID_DICT["title_bar_img"]):
            try:
                self.d(resourceId=RESOURCE_ID_DICT["title_bar_img"]).click()
            except:
                pass
        self.d(resourceId=RESOURCE_ID_DICT["mo_ni_button"]).click()

    def __open_app_goto_moni_page(self):
        # 初始化时，进入模拟界面
        self.__util_close_others()
        self.d.app_start(package_name=THS_PACKAGE_NAME, wait=True)  # 打开软件
        print("THS_APP starts successfully at.", datetime.now().strftime("%H:%M:%S"))
        # time.sleep(0.5)
        # click 自带20s等待
        self.d.xpath('//*[@content-desc="交易"]').child('/android.widget.ImageView[1]').click()
        self.d(resourceId=RESOURCE_ID_DICT["mo_ni_button"]).click()



    def __util_close_others(self):
        # 关闭掉一些不必要的弹窗
        # time.sleep(1)
        if self.__util_check_id_in_app_page(RESOURCE_ID_DICT['close_button']):
            try:
                self.d(resourceId=RESOURCE_ID_DICT['close_button']).click()
            except:
                pass
        if self.__util_check_id_in_app_page(RESOURCE_ID_DICT['ok_button']): # 这里其实容易误触
            try:
                self.d(resourceId=RESOURCE_ID_DICT['ok_button']).click()
            except:
                pass

    def __util_check_id_in_app_page(self, resource_id):
        # 从返回的字符串中判断 是否是有指定的 资源id
        _hierarchy_str = self.d.dump_hierarchy() # 返回界面信息, 如果返回的特别多的话，一点一点比较太慢了
        return resource_id in _hierarchy_str



if __name__ == "__main__":
    t = THSTrader()
    # print(t.get_balance())
    # print(t.get_position())
    print(t.buy(stock_code='000006',count=1000, price=8.10))
    print(t.sell(stock_code='000006', count=1000, price=8.10))
"""
    这个交易方式为使用 ths_trader 在安卓模拟器上模拟点击来进行交易的trader，

    参考 https://github.com/nladuo/THSTrader

    核心包为 uiautomator2， easyocr 来模拟操作和进行文字识别， 但总感觉速度较慢

    back
"""

import time
from datetime import datetime
import uiautomator2 as u2
import easyocr
from PIL import Image
from jupyter_events.validators import resources

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
}
THS_PACKAGE_NAME = "com.hexin.plat.android"

class THSTrader:
    def __init__(self, serial="emulator-5554"):
        self.d = u2.connect_usb(serial=serial)  # 模拟器
        self.reader = easyocr.Reader(lang_list=['ch_sim', 'en']) # 识别器
        self.__open_app_goto_moni_page() # 切进去
        print("THS_Trader init finished.")



    def get_balance(self):
        # 获取持仓界面信息
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

    def __back_to_moni_page(self):
        # 切回到最初的模拟炒股界面
        self.__util_close_others()
        # self.d.app_start(package_name=THS_PACKAGE_NAME) # 打开软件
        self.d.xpath('//*[@content-desc="交易"]').child('/android.widget.ImageView[1]') # 这里不写[1]也ok
        if self.__util_check_id_in_app_page(RESOURCE_ID_DICT["title_bar_img"]):
            try:
                self.d(resourceId=RESOURCE_ID_DICT["title_bar_img"]).click()
            except:
                pass
        self.d(resourceId=RESOURCE_ID_DICT["mo_ni_button"]).click()

    def __open_app_goto_moni_page(self):
        self.__util_close_others()
        self.d.app_start(package_name=THS_PACKAGE_NAME, wait=True)  # 打开软件
        print("THS_APP starts successfully at.", datetime.now().strftime("%H:%M:%S"))
        # time.sleep(0.5)
        # click 自带20s等待
        self.d.xpath('//*[@content-desc="交易"]').child('/android.widget.ImageView[1]').click()  # 这里不写[1]也ok
        self.d(resourceId=RESOURCE_ID_DICT["mo_ni_button"]).click()



    def __util_close_others(self):
        # 关闭掉一些不必要的弹窗
        # time.sleep(1)
        if self.__util_check_id_in_app_page(RESOURCE_ID_DICT['close_button']):
            try:
                self.d(resourceId=RESOURCE_ID_DICT['close_button']).click()
            except:
                pass
        if self.__util_check_id_in_app_page(RESOURCE_ID_DICT['ok_button']):
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
    print(t.get_balance())












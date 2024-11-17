"""
    这个交易方式为使用 ths_trader 在安卓模拟器上模拟点击来进行交易的trader，

    参考 https://github.com/nladuo/THSTrader

    核心包为 uiautomator2， easyocr 来模拟操作和进行文字识别， 但总感觉速度较慢
"""

import time
import uiautomator2 as u2
import easyocr
from PIL import Image
"""
        <node index="0" text="模拟" resource-id="com.hexin.plat.android:id/tab_mn" class="android.widget.TextView" package="com.hexin.plat.android" 
        content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" 
        long-clickable="false" password="false" selected="false" visible-to-user="true" bounds="[529,60][597,132]" drawing-order="2" hint="" />
        resource-id、分布关系和各种信息 可以在手机端使用 autox.js查看
"""
RESOURCE_ID_DICT = {
    "mo_ni_button" : 'com.hexin.plat.android:id/tab/mn', # 交易tab下的 "模拟" 按键
    "guan_bi_button" : "com.hexin.plat.android:id/close_btn", # 暂没见到
    "que_ding_button" : "com.hexin.plat.android:id/ok_btn", # 偶尔会弹出开的，需要点 "确定" 才能退出
}
THS_PACKAGE_NAME = "com.hexin.plat.android"

class THSTrader:
    def __init__(self, serial="emulator-5554"):
        self.d = u2.connect_usb(serial=serial)  # 模拟器
        self.reader = easyocr.Reader(lang_list=['ch_sim', 'en']) # 识别器
        self.__back_to_moni_page() # 切进去
        print("THS_Trader init finished.")

    def __back_to_moni_page(self):
        # 切回到最初的模拟炒股界面
        self.__util_close_other()
        self.d.app_start(package_name=THS_PACKAGE_NAME) # 打开软件
        self.d.xpath() # Todo

    def __util_close_other(self):
        # 关闭掉一些不必要的弹窗
        time.sleep(1)
        # if self.__util_check_app_page(RESOURCE_ID_DICT['guan_bi_button']):
        #     try:
        #         self.d(resourceId=RESOURCE_ID_DICT['guan_bi_button']).click()
        #     except:
        #         pass
        if self.__util_check_app_page(RESOURCE_ID_DICT['que_ding_button']):
            try:
                self.d(resourceId=RESOURCE_ID_DICT['que_ding_button']).click()
            except:
                pass

    def __util_check_app_page(self, resource_id):
        # 从返回的字符串中判断 是否是有指定的 资源id
        _hierarchy_str = self.d.dump_hierarchy() # 返回界面信息
        return resource_id in _hierarchy_str



if __name__ == "__main__":
    t = THSTrader()
    print(t.d.dump_hierarchy())












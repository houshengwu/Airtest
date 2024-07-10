# -*- encoding=utf8 -*-
__author__ = "10101"

import logging
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# Configure logging to suppress unnecessary output
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

class ElementTextGetter:
    def __init__(self):
        # Initialize Airtest
        auto_setup(__file__)

        # Initialize Poco for Android UI automation
        self.poco = AndroidUiautomationPoco()
        
    def get_element_text(self):
        index = 2
        while True:
            element = self.poco('com.tencent.mobileqq:id/ivTitleBtnLeft').sibling()[index]
            ee = element.get_text()
            print(index)
            if ee:
                print(ee)
                break  # 如果获取到文本则退出循环
            else:
                index += 1  # 如果未获取到文本，则增加index继续循环
                if index >= len(self.poco('com.tencent.mobileqq:id/ivTitleBtnLeft').sibling()):
                    break  # 如果index超出了元素列表的范围，则退出循环
    
# 示例化类对象
text_getter = ElementTextGetter()

# 调用方法获取元素文本
text_getter.get_element_text()

#获得群名称

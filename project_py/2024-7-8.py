# -*- encoding=utf8 -*-
__author__ = "10101"

import logging
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# Configure logging to suppress unnecessary output
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

# Initialize Airtest
auto_setup(__file__)

# Initialize Poco for Android UI automation
poco = AndroidUiautomationPoco()

mess = []

from collections import OrderedDict

try:
    element_type = OrderedDict([
        ('com.tencent.mobileqq:id/f24', '时间'),
        ('com.tencent.mobileqq:id/tgq', '昵称'),
        ('com.tencent.mobileqq:id/t5b', '头像'),
        ('com.tencent.mobileqq:id/nxt', '内容')
    ])

    for key in element_type:
        print(f"ID: {key}, 类型: {element_type[key]}")
        if element_type[key] == '内容':
            

            # 使用 poco 查找元素
            element = poco(key)
            if element.exists():
                for i in element:
                    text = i.child().child().child().child().get_text()
                    pos_r = i.child().child().child().child().get_position()[1]
                    if text is not None:
                        # 处理特殊字符和不可见字符
                        text = text.replace("\u200B", "").replace(u'\xa0', u' ').replace("^", "/NO").replace("\n", " ").replace("\t", " ")
                        mess.append( (text,pos_r))
                        print(f"Element text: {text}")
                    else:
                        print("Text is None")
            else:
                print("Element not found")
                
        if element_type[key] == '昵称':
            pass
                
                
                
                
                
                

except Exception as e:
    print(f"Error: {e}")

    
print(mess)
    

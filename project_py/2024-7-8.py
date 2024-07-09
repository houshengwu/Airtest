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

def clear_text(text_):
    text_c = text_.replace("\u200B", "").replace(u'\xa0', u' ').replace("^", "/NO").replace("\n", " ").replace("\t", " ")
    return text_c

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
                    elemen = i.child().child().child().child()
                    
                    if elemen.exists():

                        text = elemen.get_text()
                        pos_r = elemen.get_position()[1]
                        if text is not None:
                            # 处理特殊字符和不可见字符
                            text = clear_text(text)

                            mess.append( (text,pos_r))
                            print(f"Element text: {text}")
                        else:
                            print("Text is None")
            else:
                print("Element not found")
                
        if element_type[key] == '昵称':
            print(key,'key')
             # 使用 poco 查找元素
            element_nk = poco(key)
            if element_nk.exists():
                for ink in element_nk:

                    print(ink,'ink')

              #      ink_t = ink.child().child().offspring().get_name()
                    ink_n = ink.child().offspring()[-1].get_text()
                    pos_r = ink.child().offspring()[-1].get_position()[1]
                    
                    
                    if ink_n is not None:

                        print('ink',ink_n,pos_r)

                        mess.append( (ink_n,pos_r))

        if element_type[key] == '时间':
             # 使用 poco 查找元素
            element_t = poco(key)
            if element_t.exists():
            
                for t in element_t:

                    i_t = t.child().get_text()
                    pos_r = t.child().get_position()[1]
                    
                    
                    if i_t is not None:
                        mess.append( (i_t,pos_r))

                                 
                
except Exception as e:
    print(f"Error: {e}")

    
print(mess)
    

sorted_data = sorted(mess, key=lambda x: x[1], reverse=False)

# 输出排序后的结果
for item in sorted_data:
    print(item[0])
    
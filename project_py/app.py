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

try:
    # Example: Finding all android.widget.TextView elements and android.view.ViewGroup elements
    text_views = poco("android.widget.TextView")
    view_groups = poco("android.view.ViewGroup")
    
    # Process android.widget.TextView elements
    print(f"android.widget.TextView elements:{len(text_views)}")
    for text_view in text_views:
        text = text_view.get_text()
        print(f"TextView text: {text}")
    
    # Process android.view.ViewGroup elements
    print("\nandroid.view.ViewGroup elements:")
    for view_group in view_groups:
        # Assuming you want to print some details or handle ViewGroup elements differently
        print(f"ViewGroup details: {view_group}")
        
except Exception as e:
    print(f"Error: {e}")
poco("android.widget.FrameLayout")
try:
    # Example: Finding the element by resourceId
    element = poco("com.tencent.mobileqq:id/k9j")
    elementp = poco("com.tencent.mobileqq:id/k_2") 
    print(len(element))
    if elementp.exists():
        for ip in elementp:
            ptext =  ip.get_text().replace(u'\xa0', u' ').replace(u'\xa0 ', u' ')
            print(ptext,"ptext")
    
    if element.exists():
        for i in element:
            text = i.get_text().replace("\u200B", "").replace(u'\xa0', u' ').replace("^", "/NO")
            print(f"Element text: {text}")
    else:
        print("Element not found")
        
except Exception as e:
    print(f"Error: {e}")
    

    
print('*'*100)   

from collections import OrderedDict

try:
    element_record = poco("com.tencent.mobileqq:id/root")
    print(len(element_record), 'element_record')
    
    element_type = OrderedDict()  # 使用有序字典来保持顺序
    
    for ed in element_record:
        edc = list(ed.child())  # 将生成器对象转换为列表，保证顺序
        
        for ede in edc:
            name = ede.get_name()  # 假设这里使用正确的方法来获取元素的名称
            print(name)
            if name not in element_type:
                
                element_type[name] = None  # 使用字典的键来保持唯一性，值暂时设为 None
    
    print(list(element_type.keys()))  # 将有序字典的键转换为列表输出
    
except Exception as e:
    print(f"Error: {e}")

    




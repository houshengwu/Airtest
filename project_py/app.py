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

try:
    # Example: Finding the element by resourceId
    element = poco("com.tencent.mobileqq:id/k9j")
    elementp = poco("com.tencent.mobileqq:id/k_2") 
    print(len(element))
    if elementp.exists():
        for ip in elementp:
            ptext =  ip.get_text()
            print(ptext,"ptext")
    
    if element.exists():
        for i in element:
            text = i.get_text().replace("\u200B", "").replace("^", "/NO")
            print(f"Element text: {text}")
    else:
        print("Element not found")
        
except Exception as e:
    print(f"Error: {e}")
    
    
# 假设 RecyclerView 的资源 ID 是 com.tencent.mobileqq:id/recycler_view
recycler_view = poco("com.tencent.mobileqq:id/recycler_view")

try:
    # 使用 .offspring() 方法获取 RecyclerView 中所有子孙元素
    all_elements = recycler_view.offspring()

    for element in all_elements:
        # 假设元素是 TextView，获取其文本信息
        text = element.get_text()
        print(f"Element text: {text}")

except Exception as e:
    print(f"Error: {e}")

  
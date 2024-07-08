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
    
   
try:
    element_s = poco("androidx.recyclerview.widget.RecyclerView")
    for es in element_s:
        tes = es.child().child().child().child().child().child().get_text()
        tes_name = es.child().child().child().child().child().child().get_name()
        print(tes,'54',tes_name)

except Exception as e:
    print(e)

    
# 使用路径进行元素查找

  
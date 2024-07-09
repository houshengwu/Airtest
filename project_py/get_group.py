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


group_name = poco(textMatches='^百威尔.*$')

print(group_name.get_name())


    
element = poco('com.tencent.mobileqq:id/ivTitleBtnLeft').sibling()[2].get_text()

print(element)
    
    
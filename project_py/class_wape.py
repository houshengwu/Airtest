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


# 获取屏幕尺寸
#width, height = device().get_current_resolution()

#print(width, height,'width, height')

width, height= 1080,2340

# 定义滑动起点和终点
start_x = width // 1.2  # 屏幕宽度的中点
start_y = height * 3 // 4  # 屏幕高度的3/4处（向下偏移一些，可以根据需要调整）
end_x = width // 2  # 屏幕宽度的中点
end_y = height // 4  # 屏幕高度的1/4处（向上偏移一些，可以根据需要调整）

print((end_x, end_y),(start_x, start_y))
# 执行向上滑动操作
#swipe((end_x, end_y),(start_x, start_y),  duration=1.5)


swipe((500, 200),(800, 800),  duration=1.5)
# 可选：等待一段时间，观察滑动效果
sleep(2)

# 可选：获取滑动后的界面状态，执行其他操作


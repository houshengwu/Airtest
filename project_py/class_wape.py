import os
from airtest.core.api import *

# 获取屏幕尺寸
def get_screen_size():
    result = os.popen("adb shell wm size").read()
    width, height = result.split("Physical size: ")[-1].split("x")
    return int(width), int(height)

# 计算滑动起始点和终点
def calculate_swipe_points(screen_width, screen_height):
    start_x = screen_width // 2  # 屏幕宽度的中点
    start_y = screen_height // 4  # 屏幕高度的1/4处（向上偏移一些）
    end_x = screen_width // 2  # 屏幕宽度的中点
    end_y = screen_height * 3 // 4  # 屏幕高度的3/4处（向下偏移一些）
    return start_x, start_y, end_x, end_y

# 获取当前屏幕尺寸
screen_width, screen_height = get_screen_size()

# 计算滑动起始点和终点
start_x, start_y, end_x, end_y = calculate_swipe_points(screen_width, screen_height)

# 发送向下滑动事件
for i in range(0,10):
    adb_command = f"adb shell input swipe {start_x} {start_y} {end_x} {end_y} 500"
    os.system(adb_command)

    # 可选：等待一段时间，观察滑动效果或执行后续操作
    sleep(2)

# 可选：继续执行其他的 Airtest 测试步骤


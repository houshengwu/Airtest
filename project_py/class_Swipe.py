import os
from airtest.core.api import *


class Swipe:
    def __init__(self):
        
            # 获取当前屏幕尺寸
        self.screen_width, self.screen_height = self.get_screen_size()

        # 计算滑动起始点和终点
        self.start_x, self.start_y, self.end_x, self.end_y =self.calculate_swipe_points()
        
        
        self.swipe()


    # 获取屏幕尺寸
    def get_screen_size(self):
        result = os.popen("adb shell wm size").read()
        width, height = result.split("Physical size: ")[-1].split("x")
        return int(width), int(height)

    # 计算滑动起始点和终点
    def calculate_swipe_points(self):
        start_x = self.screen_width // 2  # 屏幕宽度的中点
        start_y = self.screen_height // 5  # 屏幕高度的1/4处（向上偏移一些）
        end_x = self.screen_width // 2  # 屏幕宽度的中点
        end_y = self.screen_height * 3 // 4  # 屏幕高度的3/4处（向下偏移一些）
        return start_x, start_y, end_x, end_y



    # 发送向下滑动事件
    def swipe(self):
        adb_command = f"adb shell input swipe {self.start_x} {self.start_y} {self.end_x} {self.end_y} 500"
        os.system(adb_command)
    # 可选：继续执行其他的 Airtest 测试步骤
    
swipe = Swipe()


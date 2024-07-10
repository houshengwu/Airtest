# -*- encoding=utf8 -*-
__author__ = "10101"

import logging
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from collections import OrderedDict

# Configure logging to suppress unnecessary output
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

class ElementAnalyzer:
    def __init__(self):
        # Initialize Airtest
        auto_setup(__file__)

        # Initialize Poco for Android UI automation
        self.poco = AndroidUiautomationPoco()

    def analyze_elements(self):
        try:
            element_record = self.poco("com.tencent.mobileqq:id/root")
            print(len(element_record), 'element_record')
            
            element_type = OrderedDict()  # 使用有序字典来保持顺序
            
            for ed in element_record:
                edc = list(ed.child())  # 将生成器对象转换为列表，保证顺序
                
                for ede in edc:
                    name = ede.get_name()  # 假设这里使用正确的方法来获取元素的名称
                    pos = ede.get_position()[0]  # 获取元素的位置信息
                    
                    if name not in element_type:
                        if float(pos) == 0.5:
                            element_type[name] = f"时间"
                        elif float(pos) < 0.08:
                            element_type[name] = f"头像"
                        elif 0.32 > float(pos) >= 0.08:
                            element_type[name] = f"昵称"
                        elif 0.8 > float(pos) >= 0.35:
                            element_type[name] = f"内容"
            
            return element_type  # 返回分析结果
        
        except Exception as e:
            print(f"Error: {e}")
            return None

# 示例代码：创建类实例并调用方法
if __name__ == "__main__":
    analyzer = ElementAnalyzer()
    analyzed_elements = analyzer.analyze_elements()
    if analyzed_elements:
        print("分析结果:")
        for name, category in analyzed_elements.items():
            print(f"{name}: {category}")
    else:
        print("分析失败，请检查日志信息。")

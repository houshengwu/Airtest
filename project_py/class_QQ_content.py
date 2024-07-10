import os
import sys
import logging
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# Configure logging to suppress unnecessary output
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

class ExtractContent:
    def __init__(self, element_type):
        # Initialize Airtest
        auto_setup(__file__)

        # Initialize Poco for Android UI automation
        self.poco = AndroidUiautomationPoco()
        self.element_type = element_type
        # List to store analyzed messages
        self.messages = []

    def clear_text(self, text_):
        """Clean up text from special characters and whitespaces."""
        text_c = text_.replace("\u200B", "").replace(u'\xa0', u' ').replace("^", "/NO").replace("\n", " ").replace("\t", " ").replace("\u2005", " ")
        return text_c

    def analyze_elements(self):
        for key in self.element_type:
            print(f"ID: {key}, 类型: {self.element_type[key]}")
            if self.element_type[key] == '内容':
                # Process elements of type '内容'
                element = self.poco(key)
                if element.exists():
                    for i in element:
                        elemen = i.child().child().child().child()
                        if elemen.exists():
                            text = elemen.get_text()
                            pos_r = elemen.get_position()[1]
                            if text is not None:
                                # Clean up text
                                text = self.clear_text(text)
                                self.messages.append((text, pos_r, '内容'))
                              #  print(f"Element text: {text}")
                            else:
                                print("Text is None")
                else:
                    print("Element not found")

            elif self.element_type[key] == '昵称':
                # Process elements of type '昵称'
                element_nk = self.poco(key)
                if element_nk.exists():
                    for ink in element_nk:
                        ink_e = ink.child().offspring()[-1]
                        if ink_e.exists():
                            ink_n = ink_e.get_text()
                            pos_r = ink_e.get_position()[1]
                            if ink_n is not None:
                                self.messages.append((ink_n, pos_r, '昵称'))
                              #  print('昵称', ink_n, pos_r)

            elif self.element_type[key] == '时间':
                # Process elements of type '时间'
                element_t = self.poco(key)
                if element_t.exists():
                    for t in element_t:
                        t_el = t.child()
                        if t_el.exists():
                            i_t = self.clear_text(t_el.get_text())
                            pos_r = t_el.get_position()[1]
                            if i_t is not None:
                                self.messages.append((i_t, pos_r, '时间'))

    def sort_and_print_messages(self):
        sorted_data = sorted(self.messages, key=lambda x: x[1], reverse=False)
        # 输出排序后的结果
        for item in sorted_data:
            print(item)

if __name__ == "__main__":
    # 获取当前脚本所在的目录路径
    current_dir = os.path.dirname(__file__)
    # 将当前目录添加到系统路径中
    sys.path.append(current_dir)
    # Import ElementAnalyzer from class_get_type module
    from class_get_type import ElementAnalyzer

    # 创建 ElementAnalyzer 的实例
    analyzer = ElementAnalyzer()
    # 调用 analyze_elements 方法
    analyzed_elements = analyzer.analyze_elements()

    # 处理分析结果
    if analyzed_elements:
        print(analyzed_elements)
        print("分析结果:")
        for name, category in analyzed_elements.items():
            print(f"-->{name}: {category}")
    else:
        
        print("分析失败，请检查日志信息。")

    # 实例化 ExtractContent 类对象
    extractor = ExtractContent(analyzed_elements)

    # 调用方法执行分析和输出
    extractor.analyze_elements()
    extractor.sort_and_print_messages()

import os
import sys
import logging
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import re
# 配置日志记录以减少不必要的输出
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

class ExtractContent:
    def __init__(self, element_type):
        # 初始化 Airtest
        auto_setup(__file__)

        # 初始化 Poco 用于 Android UI 自动化
        self.poco = AndroidUiautomationPoco()
        self.element_type = element_type
        # 存储分析后的消息的列表
        self.messages = []
        self.send_time = None
        self.tidy_list = None
        self.analyze_elements()
        self.sorted_data_with_index = self.sort_and_print_messages()
        self.out_put_detail()
        
        
        

    def clear_text(self, text_):
        #"""清理文本，去除特殊字符和空白符。"""
        #"""清理文本，去除以\u开头的四位十六进制编码后跟一个空格。"""
        # 使用正则表达式替换所有特殊字符和空白符为一个空格
        text_ = re.sub(r'[\u200B\u00a0\n\t\u2005\u2705\u2795\x00]', ' ', text_)
        
    # 使用正则表达式替换所有以\u开头的四位十六进制编码后跟一个空格为一个空格
        pattern = r'\\u[0-9a-fA-F]{4}\s'
        text_c = re.sub(pattern, ' ', text_)
        return text_c
    
    def analyze_elements(self):
        """分析不同类型的元素并提取信息。"""
        for key in self.element_type:
            if self.element_type[key] == '内容':
                # 处理类型为 '内容' 的元素
                element = self.poco(key)
                if element.exists():
                    for i in element:
                        elemen = i.child().child().child().child()
                        if elemen.exists():
                            text = elemen.get_text()
                            pos_r = elemen.get_position()[1]
                            if text is not None:
                                # 清理文本
                                text = self.clear_text(text)
                                self.messages.append((text, pos_r, '内容'))
                else:
                    print("未找到元素")

            elif self.element_type[key] == '昵称':
                # 处理类型为 '昵称' 的元素
                element_nk = self.poco(key)
                if element_nk.exists():
                    for ink in element_nk:
                        ink_e = ink.child().offspring()[-1]
                        if ink_e.exists():
                            ink_n = ink_e.get_text()
                            pos_r = ink_e.get_position()[1]
                            if ink_n is not None:
                                self.messages.append((ink_n, pos_r, '昵称'))

            elif self.element_type[key] == '时间':
                # 处理类型为 '时间' 的元素
                element_t = self.poco(key)
                if element_t.exists():
                    for t in element_t:
                        t_el = t.child()
                        if t_el.exists():
                            i_t = self.clear_text(t_el.get_text())
                            pos_r = t_el.get_position()[1]
                            if i_t is not None:
                                print(i_t,'i_t')
                                self.send_time = i_t
                                self.messages.append((i_t, pos_r, '时间'))

    def sort_and_print_messages(self):
        """对消息进行排序并打印。"""
        sorted_data = sorted(self.messages, key=lambda x: x[1], reverse=False)
        sorted_data_with_index = [(idx + 1, item) for idx, item in enumerate(sorted_data)]
        tidy_list = []
        print("排序后的消息:")
        for idx, item in sorted_data_with_index:
            pass
        #    print(f"{idx}. {item}")
        return sorted_data_with_index
    
    def out_put_detail(self):       
        tidy_list = []
        for idx, item in self.sorted_data_with_index:
            # 如果项目类型为 '内容' 且索引大于 1，则获取详细信息
            if item[2] == '内容' and idx > 1:
                
                
                while True:
                    ic = self.get_detail(idx-1)
                    if ic[2] == "昵称":
                        tidy_list.append([self.get_sendtime(idx),item[0], item[2], ic[0]])
                        break
                    else:
                        idx-=1
        
        self.tidy_list = tidy_list

    
    def get_detail(self, idx):
        """获取指定索引处的详细信息。"""
        if 1 <= idx <= len(self.sorted_data_with_index):
            item = self.sorted_data_with_index[idx - 1][1]
            return item
        else:
            print(f"索引 {idx} 超出范围。")
            
    def get_sendtime(self, idx):
        if 1 <= idx <= len(self.sorted_data_with_index):
            while idx >= 1:
                if len(self.sorted_data_with_index) > 2 :
                    print(f'这里##{idx}')
                    if self.sorted_data_with_index[idx - 3][1][2] == '时间':
                        return  self.sorted_data_with_index[idx - 3][1][0]
                
                    else:
                        idx -= 1
                    
        else:
            raise IndexError("Index out of range")



                    
                
        
            
            

if __name__ == "__main__":
    # 获取当前脚本所在的目录路径
    current_dir = os.path.dirname(__file__)
    # 将当前目录添加到系统路径中
    sys.path.append(current_dir)
    # 从 class_get_type 模块导入 ElementAnalyzer 类
    from class_get_type import ElementAnalyzer

    # 创建 ElementAnalyzer 的实例
    analyzer = ElementAnalyzer()
    # 调用 analyze_elements 方法进行元素分析
    analyzed_elements = analyzer.analyzed_elements



    # 实例化 ExtractContent 类对象，并传入分析结果
    extractor = ExtractContent(analyzed_elements)

    print('*'*100)
    print(extractor.sorted_data_with_index)
    
    # 示例：获取索引为 2 的项目的详细信息
    extractor.get_detail(1)




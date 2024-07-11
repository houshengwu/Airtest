# -*- encoding=utf8 -*-
__author__ = "10101"
# 取出元素 时间、昵称、头像、内容的元素
import logging
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from collections import OrderedDict
# 获取当前脚本所在的目录路径
current_dir = os.path.dirname(__file__)
# 将当前目录添加到系统路径中
sys.path.append(current_dir)
# Configure logging to suppress unnecessary output
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

from class_mysql import UpLoadMysql #上传数据库
from class_QQ_content import ExtractContent  #QQ信息提取
from class_get_type import ElementAnalyzer #群聊的元素码提取
from class_Swipe import Swipe #向下滑动
from get_group import ElementTextGetter  #提取群名称

# 创建 ElementAnalyzer 的实例
analyzer = ElementAnalyzer()
# 调用 analyze_elements 方法进行元素分析
analyzed_elements = analyzer.analyzed_elements 


text_getter = ElementTextGetter()
group_name = text_getter.get_element_text() #获取群名称
# 实例化 ExtractContent 类对象，并传入分析结果


cache_data = []

for i in range(0,100):
    extractor = ExtractContent(analyzed_elements)  #获得可见元素文本
    data_list = extractor.tidy_list
    
    for i_cache in data_list:
        cache_data.append(i_cache[1])
        if len(cache_data) > 5:
            del cache_data[0]

    print(cache_data)

        


    for data in data_list:
        if data[0] not  in cache_data:
            data.append(group_name)
            upload_mysql = UpLoadMysql(data) # 上传

    swipe = Swipe()
    swipe.swipe()



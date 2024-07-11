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


from class_mysql import UpLoadMysql


data = ['DSPIC30F2010-30I/SO  长期排单，价优，支持实单，需求联系，支持各种检测', '深圳市荃微科技刘leo']

upload_mysql = UpLoadMysql(data)

# Call the upload method to insert data into MySQL
upload_mysql.upload()
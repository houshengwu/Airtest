# 获取当前脚本所在的目录路径
current_dir = os.path.dirname(__file__)
# 将当前目录添加到系统路径中
sys.path.append(current_dir)
from class_get_type import ElementAnalyzer
# 创建 ElementAnalyzer 的实例
analyzer = ElementAnalyzer()
# 调用 analyze_elements 方法
analyzed_elements = analyzer.analyze_elements()
# 处理分析结果
if analyzed_elements:
    print("分析结果:")
    for name, category in analyzed_elements.items():
        print(f"{name}: {category}")
else:
    print("分析失败，请检查日志信息。")

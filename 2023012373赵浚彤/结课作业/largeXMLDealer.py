"""
2023012373赵浚彤
2025春季学期python
结课作业
"""
from lxml import etree
import os

# 定义 largeXMLDealer 类
class LargeXMLHandler:
    def __init__(self):
        """类的构造函数，初始化对象时调用"""
        pass

    def process_xml(self, file_path, element_callback):
        """
        迭代解析 XML 文件，并在遇到每个元素的结束标签时调用 element_callback 函数。
        该方法会处理文档中的所有元素。
        """
        # 检查文件是否存在
        if not os.path.isfile(file_path):
            print(f"文件: {file_path} 不存在。")
            return

        try:
            # 使用 etree.iterparse 迭代解析 XML 文件
            context = etree.iterparse(file_path, events=('end',), recover=True)
            for event, element in context:
                if element_callback:
                    try:
                        # 调用回调函数处理元素
                        element_callback(element)
                    except Exception as e:
                        print(f"处理元素 <{element.tag if element is not None else 'None'}> 的回调函数出错: {e}")
                if element is not None:
                    # 清理元素以节省内存
                    element.clear()
        except etree.XMLSyntaxError as e:
            print(f"解析文件 {file_path} 时出现 XML 语法错误: {e}")
        except Exception as e:
            print(f"解析文件 {file_path} 时发生意外错误: {e}")

###################################################################################
##
##  Import
##
###################################################################################
from lxml import etree
from os import path

###################################################################################
##
##  Class
##
###################################################################################

class largeXMLDealer:

    def __init__(self):
        """构造函数"""
        pass

    def parse(self, fileName, func_for_element):
        """
        迭代解析一个XML文件，并在遇到每个元素的结束标签时调用 func_for_element。
        此方法处理文档中的所有元素。
        """
        if not path.isfile(fileName):
            print(f"文件: {fileName} 不存在。")
            return

        try:
            context = etree.iterparse(fileName, events=('end',), recover=True)
            for event, elem in context:
                if func_for_element:
                    try:
                        # 将元素传递给回调函数
                        func_for_element(elem)
                    except Exception as e:
                        print(f"处理元素 <{elem.tag if elem is not None else 'None'}> 的回调函数出错: {e}")
                        pass
                if elem is not None: # 确保 elem 不为 None 后再进行清理
                    elem.clear()
        except etree.XMLSyntaxError as e:
            print(f"解析文件 {fileName} XML语法错误: {e}")
            pass
        except Exception as e: # 捕获解析过程中其他潜在的错误
            print(f"解析文件 {fileName} 时发生意外错误: {e}")
            pass
"""
@Author: Weizhi Wang
@Date: 2025-06-03
@Description: Python 解析大型 XML 文件
"""

from lxml import etree
from os import path

class XMLStreamProcessor:
    """大型XML文件流式处理类"""
    
    def __init__(self):
        """初始化处理器"""
        pass

    def process(self, file_path, element_handler):
        """
        流式解析XML文件，处理每个完整元素
        :param file_path: 待解析的XML文件路径
        :param element_handler: 元素处理回调函数
        """
        # 检查文件是否存在
        if not path.isfile(file_path):
            print(f"错误: 文件 '{file_path}' 不存在")
            return

        try:
            # 创建迭代解析器，仅处理结束事件并启用恢复模式
            parser = etree.iterparse(file_path, events=('end',), recover=True)
            
            # 遍历解析结果
            for _, element in parser:
                if element_handler and element is not None:
                    try:
                        # 调用用户处理函数
                        element_handler(element)
                    except Exception as e:
                        # 处理异常
                        tag_name = element.tag if hasattr(element, 'tag') else '未知元素'
                        print(f"警告: 处理元素 <{tag_name}> 时出错 - {str(e)}")
                    finally:
                        # 清理已处理元素以释放内存
                        element.clear()
                        parent = element.getparent()
                        if parent is not None:
                            parent.remove(element)
            
            # 清理根元素
            root = parser.root
            if root is not None:
                root.clear()
                
        except etree.XMLSyntaxError as e:
            print(f"XML语法错误: {str(e)}")
        except Exception as e:
            print(f"解析XML时发生意外错误: {str(e)}")
        finally:
            # 确保资源被释放
            if 'parser' in locals():
                del parser

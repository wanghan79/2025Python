from lxml import etree
from os import path


class largeXMLProcessor:
    """大型XML文件处理类"""

    def __init__(self):
        """构造函数"""
        pass

    def process_xml(self, file_path, element_callback):
        """
        迭代解析XML文件，并在遇到每个元素的结束标签时调用处理函数
        :param file_path: XML文件路径
        :param element_callback: 元素处理回调函数
        """
        # 验证文件存在性
        if not path.isfile(file_path):
            print(f"错误: 文件 '{file_path}' 不存在")
            return

        try:
            # 创建迭代解析上下文
            parsing_context = etree.iterparse(file_path, events=('end',), recover=True)

            # 遍历XML元素
            for event, xml_element in parsing_context:
                if element_callback and xml_element is not None:
                    try:
                        # 调用元素处理函数
                        element_callback(xml_element)
                    except Exception as e:
                        # 异常处理
                        tag = xml_element.tag if hasattr(xml_element, 'tag') else '未知标签'
                        print(f"警告: 处理元素 <{tag}> 时出错 - {str(e)}")
                    finally:
                        # 清理元素释放内存
                        xml_element.clear()
                        parent = xml_element.getparent()
                        if parent is not None:
                            parent.clear()

            # 清理根元素
            root = parsing_context.root
            if root is not None:
                root.clear()

        except etree.XMLSyntaxError as e:
            print(f"XML语法错误: {str(e)}")
        except Exception as e:
            print(f"解析XML时发生意外错误: {str(e)}")
        finally:
            # 确保上下文被清理
            if 'parsing_context' in locals():
                del parsing_context
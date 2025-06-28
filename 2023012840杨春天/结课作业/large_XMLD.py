from lxml import etree
from os import path


class largeXMLDealer:
    """大型XML文件处理类"""

    def __init__(self):
        """构造函数"""
        pass

    def parse(self, fileName, func_for_element):
        """
        迭代解析XML文件，并在遇到每个元素的结束标签时调用处理函数
        :param fileName: XML文件路径
        :param func_for_element: 元素处理回调函数
        """
        # 验证文件存在性
        if not path.isfile(fileName):
            print(f"错误: 文件 '{fileName}' 不存在")
            return

        try:
            # 创建迭代解析上下文
            context = etree.iterparse(fileName, events=('end',), recover=True)

            # 遍历XML元素
            for event, elem in context:
                if func_for_element and elem is not None:
                    try:
                        # 调用元素处理函数
                        func_for_element(elem)
                    except Exception as e:
                        # 异常处理
                        tag = elem.tag if hasattr(elem, 'tag') else '未知标签'
                        print(f"警告: 处理元素 <{tag}> 时出错 - {str(e)}")
                    finally:
                        # 清理元素释放内存
                        elem.clear()
                        parent = elem.getparent()
                        if parent is not None:
                            parent.clear()

            # 清理根元素
            root = context.root
            if root is not None:
                root.clear()

        except etree.XMLSyntaxError as e:
            print(f"XML语法错误: {str(e)}")
        except Exception as e:
            print(f"解析XML时发生意外错误: {str(e)}")
        finally:
            # 确保上下文被清理
            if 'context' in locals():
                del context
from lxml import etree
from os import path

class LargeXMLDealer:
    """
    用于解析超大 XML 文件，并对匹配的元素执行用户自定义回调。
    """
    def __init__(self):
        pass

    def parse(self, file_name, func_for_element):
        """
        解析指定 XML 文件，对每个元素调用用户函数。
        """
        if not path.isfile(file_name):
            print(f"[错误] 文件 '{file_name}' 不存在")
            return

        try:
            context = etree.iterparse(file_name, events=('end',), recover=True)
            for event, elem in context:
                if func_for_element:
                    try:
                        func_for_element(elem)
                    except Exception as e:
                        print(f"[回调错误] <{elem.tag}>: {e}")
                if elem is not None:
                    elem.clear()
        except etree.XMLSyntaxError as e:
            print(f"[解析错误] XML语法错误: {e}")
        except Exception as e:
            print(f"[解析错误] 发生异常: {e}")

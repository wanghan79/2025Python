"""
大文件 XML 解析器装饰器实现
"""

from lxml import etree
from os import path
"""
此为结课作业
    """
from optparse import OptionParser


class XMLDecoratorParser:
    """
    用作装饰器的大型 XML 文件解析器。
    通过 __init__ 初始化参数，__call__ 将解析逻辑注入被装饰函数。

    用法示例：
        >>> @XMLDecoratorParser("example.xml", "entry")
    """

    def __init__(self, xml_path, tag_name):
        """
        初始化装饰器。

        参数:
            xml_path: XML 文件的路径
            tag_name: 想要解析的目标标签（不含命名空间）
        """
        self.xml_path = xml_path
        self.tag_name = tag_name

    def __call__(self, target_func):
        """
        装饰器调用接口

        参数:
            target_func: 被修饰的函数，用于处理单个 XML 元素

        返回:
            包装后的函数，执行时自动完成 XML 解析与处理
        """
        def wrapped(*args, **kwargs):
            return self._parse_and_apply(self.xml_path, self.tag_name, target_func)

        return wrapped

    def _parse_and_apply(self, xml_file, target_tag, handler=None):
        """
        核心解析方法。

        参数:
            xml_file: XML 文件名
            target_tag: 目标元素标签
            handler: 外部传入的处理函数，用于操作单个解析元素

        返回:
            成功处理的元素数量
        """
        if not path.isfile(xml_file) or not xml_file.endswith(".xml"):
            raise FileNotFoundError("未找到合法的 XML 文件。")

        parsed_count = 0
        event_types = ('end',)
        namespace = self._extract_namespace(xml_file)
        namespaced_tag = f"{{{namespace}}}{target_tag}"

        parser = etree.iterparse(xml_file, events=event_types, tag=namespaced_tag)

        for _, element in parser:
            try:
                handler(element)
            except Exception:
                raise RuntimeError("处理元素的函数发生异常。")
            finally:
                element.clear()
                parsed_count += 1
                while element.getprevious() is not None:
                    del element.getparent()[0]

        del parser
        return parsed_count

    def _extract_namespace(self, xml_file):
        """
        获取命名空间（仅取第一个）

        参数:
            xml_file: XML 文件路径

        返回:
            命名空间 URI 字符串
        """
        if not path.isfile(xml_file) or not xml_file.endswith(".xml"):
            raise FileNotFoundError("未找到合法的 XML 文件。")

        context = etree.iterparse(xml_file, events=('start-ns',))
        namespace_uri = ''
        for _, ns_tuple in context:
            _, namespace_uri = ns_tuple
            break  # 只取第一个命名空间
        del context
        return namespace_uri

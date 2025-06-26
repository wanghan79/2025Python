"""
本程序实现可作装饰器的大型 XML 文件解析器

作者：李超平
用途：Python 程序设计课结课作业
"""

from lxml import etree
from os import path
from optparse import OptionParser


class LargeXMLParser:
    """
    可作装饰器的大型 XML 文件解析器
    __init__函数接收装饰器的初始化参数初始化装饰器
    __call__函数将类包装成装饰器

    Examples:
        >>> @LargeXMLParser("P00734.xml", "taxon")
    """

    def __init__(self, filename, elemTag):
        """
        Constructor

        参数:
            filename: XML 文件路径
            elemTag: 要解析的目标标签名（不含命名空间）
        """
        self.filename = filename
        self.elemTag = elemTag

    def __call__(self, func):
        """
        允许将本类实例作为装饰器使用

        参数:
            func: 用于处理解析元素的函数

        返回:
            function: 包装后的函数，自动执行解析操作
        """
        def wrapper(*args, **kwargs):
            return self.parse(self.filename, self.elemTag, func)

        return wrapper

    def parse(self, fileName, elemTag, func4Element=None):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            # Call the outside function to deal with the element here
            try:
                func4Element(elem)
            except Exception:
                raise Exception("Something wrong in function parameter: func4Element")
            finally:
                elem.clear()
                count = count + 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        # Return how many elements had been parsed
        return count

    def _getNamespace(self, fileName):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            # print("%s, %d"%(elem, len(elem)))
            break
        del context
        return result



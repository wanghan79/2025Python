"""
此为 Python 程序设计课平时作业二：随机数据生成

作者：梁博芳
用途：Python 程序设计课结课作业
"""

from lxml import etree
from os import path

class LargeXMLParser:
    """
    可作装饰器的大型 XML 文件解析器
    __init__函数接收装饰器的初始化参数初始化装饰器
    __call__函数将类包装成装饰器
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
        """
        解析 XML 文件中指定标签的内容

        参数:
            fileName: XML 文件的完整路径
            elemTag: 目标元素标签名
            func4Element: 用于处理每个元素的函数
        """
        if not path.isfile(fileName) or not fileName.endswith(".xml"):
            raise FileNotFoundError(f"文件 {fileName} 不存在或不是 XML 文件")

        count = 0
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=("end",), tag=ns + elemTag)

        for event, elem in context:
            try:
                if func4Element:
                    func4Element(elem)
            except Exception as e:
                raise RuntimeError(f"处理元素时出错: {e}")
            finally:
                elem.clear()
                count += 1
                # 删除前面的兄弟节点，防止内存泄漏
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        print(f"已成功解析 {count} 个 <{elemTag}> 元素")
        return count

    def _getNamespace(self, fileName):
        """
        获取 XML 文件的命名空间

        参数:
            fileName: XML 文件的完整路径

        返回:
            str: 命名空间字符串
        """
        if not path.isfile(fileName) or not fileName.endswith(".xml"):
            raise FileNotFoundError(f"文件 {fileName} 不存在或不是 XML 文件")

        result = ''
        context = etree.iterparse(fileName, events=("start-ns",))
        for event, elem in context:
            prefix, uri = elem
            result = uri
            break  # 只需要第一个命名空间声明
        del context
        return result

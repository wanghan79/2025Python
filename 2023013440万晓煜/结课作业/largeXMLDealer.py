from lxml import etree
from os import path
from functools import wraps


class largeXMLDealer:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, fileName, elemTag):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("输入的文件不存在或不是合法XML文件")

        count = 0
        ns = self._getNamespace(fileName)
        ns_tag = f"{{{ns}}}{elemTag}"

        context = etree.iterparse(fileName, events=('end',), tag=ns_tag)

        for event, elem in context:
            try:
                self.func(elem)
            except Exception as e:
                raise Exception(f"被修饰函数出错: {e}")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):
        context = etree.iterparse(fileName, events=('start-ns',))
        for event, elem in context:
            prefix, uri = elem
            del context
            return uri
        return ""

    def extract_structure(self, element):
        """递归打印元素结构及内容，并统计标签数量"""
        tag_counts = {}

        def _extract(elem, level=0):
            tag = elem.tag
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            print("  " * level + f"<{tag}>")
            if elem.text and elem.text.strip():
                print("  " * (level + 1) + f"Text: {elem.text.strip()}")
            for child in elem:
                _extract(child, level + 1)
            print("  " * level + f"</{tag}>")

        _extract(element)

        print("标签统计：")
        for tag, count in tag_counts.items():
            print(f"{tag}: {count}")

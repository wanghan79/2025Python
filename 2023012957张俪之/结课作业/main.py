"""
    author: Zhang Lizhi
    date: 2025.06.03
    name: 结课作业
    run: python main.py fileName elemTag
"""

import sys
from lxml import etree
from os import path
from functools import wraps

class largeXMLDealer:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, fileName, elemTag):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        es = ('end', )
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns
        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            try:
                self.func(elem)
            except Exception as e:
                raise Exception(f"Something wrong in function parameter: {e}")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):
        # 检查文件是否存在且是 XML 文件
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")
        result = ''
        es = ('start-ns', )
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            break
        del context
        return result

    def extract_structure(self, element):
        """提取并打印 XML 元素的结构和文本内容。"""
        tag_counts = {}

        def _extract_structure(elem, level=0):
            """递归提取元素结构。"""
            nonlocal tag_counts
            tag = elem.tag
            if tag not in tag_counts:
                tag_counts[tag] = 0
            tag_counts[tag] += 1

            print("  " * level + f"<{tag}>")

            if elem.text and elem.text.strip():
                print("  " * (level + 1) + f"Text: {elem.text.strip()}")
            for child in elem:
                _extract_structure(child, level + 1)

            print("  " * level + f"</{tag}>")

        # 递归提取结构
        _extract_structure(element)

        # 打印标签统计信息
        print("\n标签统计：")
        for tag, count in tag_counts.items():
            print(f"{tag}: {count}")


@largeXMLDealer
def dealwithElement(elem):
    """处理每个 XML 元素，提取其结构"""
    dealer = largeXMLDealer(lambda x: None) 
    dealer.extract_structure(elem)


if __name__ == "__main__":
    fileName = sys.argv[1]
    elemTag = sys.argv[2]
    count = dealwithElement(fileName, elemTag)
    print(f"\n总共有 '{elemTag}' 标签的数量: {count}")
    

# python C:\Users\MAC\Desktop\python1\Python\结课作业\exercise3.py C:\Users\MAC\Desktop\python1\Python\结课作业\P00734.xml accession

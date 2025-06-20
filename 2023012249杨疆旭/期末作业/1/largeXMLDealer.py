
#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

from lxml import etree
from os import path

class largeXMLDealer:
    """用于解析大型XML文件的类"""

    def __init__(self):
        pass

    def parse(self, fileName, elemTag, func4Element=None):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError(f"文件 {fileName} 不存在或不是 XML")

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            try:
                func4Element(elem)
            except Exception:
                raise Exception("处理元素的函数出错")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            return elem[1]

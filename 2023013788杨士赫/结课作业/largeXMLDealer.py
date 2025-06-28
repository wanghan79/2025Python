#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

from lxml import etree
from os import path
from functools import wraps


class largeXMLDealer:
    """
    XML大文件解析器
    """

    def __init__(self):

    def parse_decorator(self, xml_file, tag_name):
        """
        解析XML文件的装饰器
        参数:
            xml_file: 要解析的XML文件路径
            tag_name: 要提取的标签名
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not path.isfile(xml_file) or not xml_file.endswith("xml"):
                    raise FileNotFoundError(f"文件不存在或不是有效的XML文件: {xml_file}")

                count = 0
                ns = self._getNamespace(xml_file)
                ns_prefix = "{%s}" % ns if ns else ""

                context = etree.iterparse(xml_file, events=('end',), tag=ns_prefix + tag_name)

                for event, elem in context:
                    try:
                        func(elem, *args, **kwargs)
                    except Exception as e:
                        print(f"处理元素时出错: {e}")
                    finally:
                        elem.clear()
                        count += 1
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]
                del context
                print(f"已成功解析 {count} 个XML元素.")
                return count

            return wrapper

        return decorator

    def _getNamespace(self, fileName):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            break
        del context
        return result
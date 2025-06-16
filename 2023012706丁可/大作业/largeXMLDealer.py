#!/usr/bin/env python
# coding:utf-8
"""
XML解析装饰器模块，用于处理大型XML文件并记录解析的节点数量
"""

from lxml import etree
from os import path
from functools import wraps


class XMLParserDecorator:
    """
    类装饰器，接收要解析的XML元素标签列表
    """
    def __init__(self, elemTags):
        if isinstance(elemTags, str):
            self.elemTags = [elemTags]  # 兼容单个标签的情况
        else:
            self.elemTags = elemTags

    def __call__(self, func):
        @wraps(func)
        def wrapper(fileName, *args, **kwargs):
            """
            包装函数，实现XML解析和计数功能
            """
            if not path.isfile(fileName) or not fileName.endswith("xml"):
                raise FileNotFoundError(f"XML file not found: {fileName}")

            # 初始化计数器
            counts = {tag: 0 for tag in self.elemTags}
            contents = {tag: [] for tag in self.elemTags}

            es = ('end',)

            # 获取命名空间
            ns = self._get_namespace(fileName)

            # 构造所有要处理的标签（带命名空间）
            actual_tags = {}
            for tag in self.elemTags:
                if ns:
                    actual_tags[tag] = f"{{{ns}}}{tag}"
                else:
                    actual_tags[tag] = tag

            context = etree.iterparse(fileName, events=es)

            for event, elem in context:
                for tag in self.elemTags:
                    if elem.tag == actual_tags[tag]:
                        try:
                            # 获取元素内容
                            if elem.text and elem.text.strip():
                                content = elem.text.strip()
                            else:
                                content = ''.join(elem.itertext()).strip()

                            if content:
                                contents[tag].append(content)
                                counts[tag] += 1
                        except Exception as e:
                            raise Exception(f"Error in element processing function: {str(e)}")
                        finally:
                            elem.clear()
                            while elem.getprevious() is not None:
                                del elem.getparent()[0]

            del context

            # 打印结果
            for tag in self.elemTags:
                print(f"\nFound {counts[tag]} '{tag}' elements:")
                for i, content in enumerate(contents[tag], 1):
                    print(f"  {i}. {content}")

            return counts

        return wrapper

    def _get_namespace(self, fileName):
        """
        获取XML文件的命名空间
        """
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

# 保持原有接口兼容性
xml_parser_decorator = XMLParserDecorator
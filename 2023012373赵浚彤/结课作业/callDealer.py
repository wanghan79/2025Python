#!/usr/bin/env python
# coding:utf-8
"""
2023012373赵浚彤
2025春季学期python
结课作业
"""
import largeXMLDealer
import sys
from functools import wraps


class largeXML:
    """
    类修饰器，用于将XML文件解析成树形结构
    """

    @staticmethod
    def parser(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取文件名和元素标签
            fileName = kwargs.get('fileName') or args[0]
            elemTag = kwargs.get('elemTag') or args[1]

            # 解析XML文件
            lxmld = largeXMLDealer.largeXMLDealer()
            tree = []

            # 定义处理元素的函数，将元素添加到树中
            def dealwithElement(elem):
                if isinstance(elem, object):
                    node = {
                        'tag': elem.tag,
                        'text': elem.text,
                        'attrib': elem.attrib,
                        'children': []
                    }
                    for child in elem:
                        dealwithElement(child)
                        node['children'].append(child)
                    tree.append(node)

            # 解析XML并构建树形结构
            count = lxmld.parse(fileName, elemTag, dealwithElement)
            print(f"Already parsed {count} XML elements.")

            # 调用原始函数，并传入树形结构
            return func(tree, *args, **kwargs)

        return wrapper


@largeXML.parser
def output(tree, fileName, elemTag):
    """
    输出树形结构
    """

    def print_tree(node, level=0):
        indent = "  " * level
        print(f"{indent}Tag: {node['tag']}")
        if node['text'] and node['text'].strip():
            print(f"{indent}Text: {node['text'].strip()}")
        if node['attrib']:
            print(f"{indent}Attributes: {node['attrib']}")
        for child in node['children']:
            print_tree(child, level + 1)

    for node in tree:
        print_tree(node)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer.py <fileName> <elemTag>")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    output(fileName=fileName, elemTag=elemTag)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
XML解析器：将XML文件转换为嵌套字典结构并输出完整数据树

功能：
1. 解析指定的XML文件
2. 将XML元素转换为字典结构（包括标签、属性、文本和子元素）
3. 以美观的JSON格式输出结果
"""

import json
from functools import wraps
from os import path
from lxml import etree


class XMLParser:
    """XML文件解析器"""

    @staticmethod
    def parse_to_dict(xml_file):
        """
        将XML文件解析为嵌套字典结构

        参数:
            xml_file (str): XML文件路径

        返回:
            dict: 表示XML结构的嵌套字典

        异常:
            FileNotFoundError: 文件不存在
            ValueError: 文件不是XML格式
            etree.XMLSyntaxError: XML语法错误
        """
        if not path.isfile(xml_file):
            raise FileNotFoundError(f"文件不存在: {xml_file}")
        if not xml_file.lower().endswith('.xml'):
            raise ValueError(f"文件不是XML格式: {xml_file}")

        try:
            tree = etree.parse(xml_file)
            return XMLParser._element_to_dict(tree.getroot())
        except etree.XMLSyntaxError as e:
            raise etree.XMLSyntaxError(f"XML语法错误: {e}") from e

    @staticmethod
    def _element_to_dict(element):
        """递归将XML元素转换为字典"""
        result = {
            'tag': element.tag,
            'attrib': dict(element.attrib),
            'text': element.text.strip() if element.text and element.text.strip() else None
        }

        children = [XMLParser._element_to_dict(child) for child in element]
        if children:
            result['children'] = children

        return result


def xml_file_parser(file_name):
    """
    装饰器：解析XML文件并传递给被装饰函数

    参数:
        file_name (str): 要解析的XML文件名
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            full_path = path.join(path.dirname(__file__), file_name)
            print(f"开始解析XML文件: {file_name}")

            try:
                xml_data = XMLParser.parse_to_dict(full_path)
                return func(xml_data, *args, **kwargs)
            except Exception as e:
                print(f"处理XML文件时出错: {e}")
                raise

        return wrapper

    return decorator


@xml_file_parser("P00734.xml")
def print_xml_structure(data_tree):
    """
    打印XML数据结构

    参数:
        data_tree (dict): XML数据树字典
    """
    print("\nXML数据结构（格式化输出）:\n")
    print(json.dumps(data_tree, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print_xml_structure()
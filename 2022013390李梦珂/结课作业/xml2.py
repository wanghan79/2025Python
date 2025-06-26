#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
XML 文件解析器

功能：将 XML 文件解析为嵌套字典结构，并以美观的 JSON 格式输出完整数据树。

输入：指定的 XML 文件路径
输出：格式化后的 XML 数据结构（字典格式）
"""

import json
from functools import wraps
from os import path
from lxml import etree


def parse_full_xml(xml_filename):
    """
    装饰器工厂函数：解析 XML 文件并传递数据给被装饰函数

    Args:
        xml_filename (str): 要解析的 XML 文件名

    Returns:
        function: 装饰器函数
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 构建完整文件路径
            xml_path = path.abspath(path.join(path.dirname(__file__), xml_filename))

            # 验证文件
            if not path.exists(xml_path):
                raise FileNotFoundError(f"XML 文件不存在: {xml_path}")
            if not xml_path.lower().endswith('.xml'):
                raise ValueError(f"文件类型错误，必须是 .xml 文件: {xml_path}")

            print(f"正在解析 XML 文件: {xml_filename}")

            try:
                # 解析 XML 并转换为字典结构
                xml_dict = xml_to_dict(xml_path)
                return func(xml_dict, *args, **kwargs)

            except etree.XMLSyntaxError as e:
                print(f"XML 语法错误: {e}")
                raise
            except Exception as e:
                print(f"解析 XML 时发生错误: {e}")
                raise

        return wrapper

    return decorator


def xml_to_dict(xml_path):
    """
    将 XML 文件转换为嵌套字典结构

    Args:
        xml_path (str): XML 文件路径

    Returns:
        dict: 表示 XML 结构的嵌套字典
    """
    tree = etree.parse(xml_path)
    root = tree.getroot()
    return element_to_dict(root)


def element_to_dict(element):
    """
    递归将 XML 元素转换为字典

    Args:
        element (lxml.etree.Element): XML 元素

    Returns:
        dict: 包含元素信息的字典
    """
    return {
        "tag": element.tag,
        "attrib": dict(element.attrib),
        "text": element.text.strip() if element.text and element.text.strip() else None,
        "children": [element_to_dict(child) for child in element]
    }


@parse_full_xml("P00734.xml")
def print_xml_structure(xml_data):
    """
    打印 XML 数据结构

    Args:
        xml_data (dict): XML 数据字典
    """
    print("\nXML 数据结构（格式化输出）:\n")
    print(json.dumps(xml_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print_xml_structure()
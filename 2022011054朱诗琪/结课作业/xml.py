#!/usr/bin/env python
# coding:utf-8

from lxml import etree
from os import path
from functools import wraps
import json

"""
程序功能：解析完整的xml文件为嵌套字典结构，输出输出 XML 的完整数据树结构（字典格式）。
"""

def parse_full_xml(file_name):
    """
    装饰器：解析完整 XML 文件为嵌套字典结构，并将其传递给被修饰函数。
    """
    def decorator(func):
        @wraps(func)
        def wrapper():
            full_path = path.join(path.dirname(__file__), file_name)

            if not path.isfile(full_path) or not full_path.endswith(".xml"):
                raise FileNotFoundError(f"找不到 XML 文件或文件类型不正确: {full_path}")

            print(f"开始解析 XML 文件：{file_name}")

            try:
                tree = etree.parse(full_path)
                root = tree.getroot()

                # 递归将 Element 转换成嵌套字典
                def elem_to_dict(elem):
                    return {
                        "tag": elem.tag,
                        "attrib": dict(elem.attrib),
                        "text": elem.text.strip() if elem.text and elem.text.strip() else None,
                        "children": [elem_to_dict(child) for child in elem]
                    }

                xml_data_tree = elem_to_dict(root)
                func(xml_data_tree)

            except Exception as e:
                print(f"解析过程中出错：{e}")

        return wrapper
    return decorator


@parse_full_xml("P00734.xml")  # 这里指定 XML 文件名
def output(data_tree):
    """
    被修饰函数：输出 XML 的完整数据树结构（字典格式）
    """
    print("XML 数据结构如下（格式化输出）：\n")
    print(json.dumps(data_tree, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    output()
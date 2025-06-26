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

    参数:
        file_name (str): 要解析的XML文件名

    返回:
        function: 装饰器函数
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取XML文件的完整路径
            full_path = path.join(path.dirname(__file__), file_name)

            # 验证文件是否存在且是XML文件
            if not path.isfile(full_path):
                raise FileNotFoundError(f"找不到文件: {full_path}")
            if not full_path.endswith(".xml"):
                raise ValueError(f"文件类型不正确，必须是XML文件: {full_path}")

            print(f"开始解析 XML 文件：{file_name}")

            try:
                # 解析XML文件
                tree = etree.parse(full_path)
                root = tree.getroot()

                def elem_to_dict(elem):
                    """递归将Element对象转换为字典"""
                    result = {
                        "tag": elem.tag,
                        "attrib": dict(elem.attrib),
                        "text": elem.text.strip() if elem.text and elem.text.strip() else None,
                    }

                    # 处理子元素
                    children = [elem_to_dict(child) for child in elem]
                    if children:
                        result["children"] = children

                    return result

                # 构建完整的XML数据树
                xml_data_tree = elem_to_dict(root)

                # 调用被装饰的函数并传递数据
                return func(xml_data_tree, *args, **kwargs)

            except etree.XMLSyntaxError as e:
                print(f"XML语法错误：{e}")
                raise
            except Exception as e:
                print(f"解析过程中出错：{e}")
                raise

        return wrapper

    return decorator


@parse_full_xml("P00734.xml")  # 这里指定 XML 文件名
def output(data_tree):
    """
    被修饰函数：输出 XML 的完整数据树结构（字典格式）

    参数:
        data_tree (dict): XML数据树字典
    """
    print("XML 数据结构如下（格式化输出）：\n")
    print(json.dumps(data_tree, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    output()
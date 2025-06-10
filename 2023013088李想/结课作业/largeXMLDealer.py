#!/usr/bin/env python
# coding:utf-8

from lxml import etree
from os import path


def parse_xml_elements(filename, elem_tag):
    """
    装饰器：用于处理大型XML文件中指定tag的元素
    :param filename: XML文件路径
    :param elem_tag: 需要处理的XML标签
    :return: 装饰器函数
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not path.isfile(filename) or not filename.endswith("xml"):
                raise FileNotFoundError(f"File not found or invalid XML file: {filename}")

            count = 0
            ns = _get_namespace(filename)
            full_tag = f"{{{ns}}}{elem_tag}" if ns else elem_tag

            context = etree.iterparse(filename, events=("end",), tag=full_tag)

            for event, elem in context:
                try:
                    func(elem, *args, **kwargs)  # 将XML元素传入用户处理函数
                finally:
                    elem.clear()
                    count += 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            print(f"Already parsed {count} XML elements.")
            return count

        return wrapper

    return decorator


def _get_namespace(filename):
    """
    获取XML文件的命名空间
    """
    if not path.isfile(filename) or not filename.endswith("xml"):
        raise FileNotFoundError(f"File not found or invalid XML file: {filename}")

    result = ''
    context = etree.iterparse(filename, events=("start-ns",))
    for event, elem in context:
        prefix, result = elem
        break
    del context
    return result

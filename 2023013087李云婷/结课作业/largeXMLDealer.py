#!/usr/bin/env python
# coding:utf-8

from lxml import etree
from os import path


def xml_element_processor(xml_file, target_tag):
    """
    装饰器：用于处理大型 XML 文件中指定标签的元素。
    :param xml_file: XML 文件路径
    :param target_tag: 需要处理的标签名称
    :return: 包装函数
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not path.exists(xml_file) or not xml_file.lower().endswith(".xml"):
                raise FileNotFoundError(f"无效或不存在的 XML 文件: {xml_file}")

            count = 0
            namespace = _fetch_namespace(xml_file)
            full_tag = f"{{{namespace}}}{target_tag}" if namespace else target_tag

            context = etree.iterparse(xml_file, events=("end",), tag=full_tag)

            for event, elem in context:
                try:
                    func(elem, *args, **kwargs)
                finally:
                    elem.clear()
                    count += 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            print(f"已解析 {count} 个 XML 元素")
            return count

        return wrapper

    return decorator


def _fetch_namespace(xml_path):
    """
    获取 XML 文件的命名空间
    """
    if not path.isfile(xml_path) or not xml_path.endswith("xml"):
        raise FileNotFoundError(f"无效或不存在的 XML 文件: {xml_path}")

    result = ''
    context = etree.iterparse(xml_path, events=("start-ns",))
    for event, elem in context:
        prefix, result = elem
        break
    del context
    return result

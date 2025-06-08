#!/usr/bin/env python
# coding:utf-8

"""
Author: H.Wang --<>
Purpose: XML 迭代解析修饰器
Created: 4/4/2016
Updated: 添加修饰器功能
"""

from lxml import etree
from os import path
from functools import wraps


def xml_dealer(elem_tag):
    """
    XML 迭代解析修饰器
    :param elem_tag: 要处理的XML元素标签
    """

    def decorator(process_func):
        @wraps(process_func)
        def wrapper(file_name):
            if not path.isfile(file_name) or not file_name.endswith("xml"):
                raise FileNotFoundError(f"XML file not found: {file_name}")

            ns = _get_namespace(file_name)
            full_tag = f"{{{ns}}}{elem_tag}" if ns else elem_tag

            count = 0
            context = etree.iterparse(file_name, events=('end',), tag=full_tag)

            for event, elem in context:
                try:
                    # 调用被修饰的处理函数
                    process_func(elem)
                except Exception as e:
                    raise RuntimeError(f"Processing error: {e}")
                finally:
                    # 清理元素释放内存
                    elem.clear()
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
                    count += 1

            del context
            print(f"Parsed {count} XML elements.")
            return count

        return wrapper

    return decorator


def _get_namespace(file_name):
    """获取XML文件的命名空间"""
    if not path.isfile(file_name) or not file_name.endswith("xml"):
        raise FileNotFoundError

    context = etree.iterparse(file_name, events=('start-ns',))
    for event, elem in context:
        _, namespace = elem
        if namespace:
            return namespace
        break
    del context
    return ""

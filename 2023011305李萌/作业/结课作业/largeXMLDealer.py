#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: 使用装饰器模式解析大型XML文件
  Created: 4/4/2016
  Modified: 6/30/2025
"""

from lxml import etree
from os import path
from functools import wraps
import sys


def xml_parser_decorator(file_path, elem_tag):
    """
    XML大文件解析装饰器，用于修饰数据打印函数
    
    Args:
        file_path: XML文件路径
        elem_tag: 需要解析的目标标签
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查文件有效性
            if not path.isfile(file_path) or not file_path.endswith("xml"):
                raise FileNotFoundError(f"无效的XML文件: {file_path}")
            
            count = 0
            ns = _get_namespace(file_path)
            target_tag = f"{{{ns}}}{elem_tag}" if ns else elem_tag
            
            try:
                # 使用iterparse处理大文件
                context = etree.iterparse(file_path, events=('end',), tag=target_tag)
                
                for event, elem in context:
                    try:
                        # 调用被装饰的函数处理元素
                        func(elem, *args, **kwargs)
                    except Exception as e:
                        print(f"处理元素时出错: {e}")
                    finally:
                        # 清理内存
                        elem.clear()
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]
                        count += 1
                
            except Exception as e:
                print(f"解析XML时发生错误: {e}")
            finally:
                # 释放上下文资源
                try:
                    del context
                except NameError:
                    pass
            
            print(f"已解析 {count} 个 {elem_tag} 元素")
            return count
            
        return wrapper
    return decorator


def _get_namespace(file_path):
    """获取XML文件的命名空间"""
    namespace = ''
    try:
        context = etree.iterparse(file_path, events=('start-ns',), load_dtd=True)
        for event, elem in context:
            prefix, namespace = elem
            break
    except Exception as e:
        print(f"获取命名空间时出错: {e}")
    finally:
        try:
            del context
        except NameError:
            pass
    return namespace


# 示例1: 装饰数据打印函数 - accession标签
@xml_parser_decorator('P00734.xml', 'accession')
def print_accession(elem, b_print=True):
    """打印accession元素文本"""
    if b_print and elem.text:
        print(elem.text.strip())


# 示例2: 打印sequence元素文本
@xml_parser_decorator('P00734.xml', 'sequence')
def print_sequence(elem, b_print=True):
    """打印sequence元素文本(格式化显示)"""
    if b_print and elem.text:
        # 格式化长序列为每行60字符
        text = elem.text.strip()
        for i in range(0, len(text), 60):
            print(text[i:i+60])


def main():
    """命令行入口函数"""
    if len(sys.argv) < 3:
        print("用法: python script.py <文件路径> <目标标签>")
        print("示例: python script.py P00734.xml accession")
        return
    
    file_path = sys.argv[1]
    elem_tag = sys.argv[2]
    
    # 动态创建并调用装饰器
    @xml_parser_decorator(file_path, elem_tag)
    def dynamic_print(elem):
        """动态创建的打印函数"""
        if elem.text:
            print(elem.text.strip())
    
    dynamic_print()


if __name__ == "__main__":

    main()
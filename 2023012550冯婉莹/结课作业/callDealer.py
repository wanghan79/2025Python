#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys

def dealwithElement(elem):
    """处理XML元素的函数"""
    if isinstance(elem, object):
        print(elem.text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python callDealer.py 文件名 元素标签")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    # 创建 largeXMLDealer 实例
    lxmld = largeXMLDealer.largeXMLDealer()

    # 调用 parse 方法解析 XML 文件
    try:
        count = lxmld.parse(fileName, elemTag, dealwithElement)
        print("Already parsed %d XML elements." % count)
    except FileNotFoundError as e:
        print("错误:", e)
    except Exception as e:
        print("发生错误:", e)
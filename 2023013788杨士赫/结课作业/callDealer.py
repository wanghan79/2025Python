#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys

lxmld = largeXMLDealer.largeXMLDealer()

# 使用装饰器修饰数据处理函数
@lxmld.parse_decorator(sys.argv[1], sys.argv[2])
def print_element_data(elem):
    """处理每个XML元素并打印数据"""
    print(elem.text)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    # 调用装饰函数开始解析
    print_element_data()
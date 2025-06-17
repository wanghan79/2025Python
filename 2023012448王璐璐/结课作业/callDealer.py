#!/usr/bin/env python
# coding:utf-8
"""
callDealer.py - 调用XML处理器的主程序
功能：提供命令行接口调用XML处理功能
"""

import sys
from largeXMLDealer import LargeXMLDealer

def main():
    if len(sys.argv) < 2:
        print("使用说明:")
        print("  python callDealer.py <XML文件> [选项]")
        print()
        print("选项:")
        print("  -a/--accession: 处理accession元素")
        print("  -s/--sequence:  处理sequence元素")
        print("  -f/--feature:   处理feature元素")
        print("  -t/--tree:      输出树状结构")
        return
    
    file_name = sys.argv[1]
    dealer = LargeXMLDealer()
    
    # 处理所有元素类型
    if "-a" in sys.argv or "--accession" in sys.argv:
        count = dealer.process_accession(file_name)
        print(f"已处理 {count} 个accession元素")
    
    if "-s" in sys.argv or "--sequence" in sys.argv:
        count = dealer.process_sequence(file_name)
        print(f"已处理 {count} 个sequence元素")
    
    if "-f" in sys.argv or "--feature" in sys.argv:
        count = dealer.process_feature(file_name)
        print(f"已处理 {count} 个feature元素")
    
    if "-t" in sys.argv or "--tree" in sys.argv:
        dealer.output_tree(file_name, "entry")
        print("XML树状结构已生成")

if __name__ == "__main__":
    main()
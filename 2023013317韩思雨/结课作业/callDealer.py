#!/usr/bin/env python
# coding:utf-8
import os
import sys
from largeXMLDealer import UniProtXMLParser  # 改为导入现有的 UniProtXMLParser

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')


def component_processor(xml_file, target_tag):
    """直接使用 UniProtXMLParser 解析组件"""
    parser = UniProtXMLParser()
    components = parser.parse_components(xml_file)  # 调用现有方法

    for comp in components:
        print("=" * 50)
        if comp['recommended_name']:
            print(f"组件名称: {comp['recommended_name']}")
        for i, name in enumerate(comp['alternative_names'], 1):
            print(f"备用名称{i}: {name}")
        print("=" * 50)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python callDealer.py <xml文件> <元素标签>")
        print("示例: python callDealer.py P00734.xml component")
        sys.exit(1)

    xml_file = sys.argv[1]
    target_tag = sys.argv[2]

    if target_tag == "component":
        component_processor(xml_file, target_tag)
    else:
        print(f"不支持的元素标签: {target_tag}")

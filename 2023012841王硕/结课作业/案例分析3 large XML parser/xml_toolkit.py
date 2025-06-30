#!/usr/bin/env python
# coding:utf-8

import argparse
from lxml import etree
import random
import string
import sys


def StatisticsManager(*operations):
    """
    统计操作装饰器，根据指定的操作计算数值统计结果
    支持的操作：
    1: 最大值 (MAX)
    2: 最小值 (MIN)
    3: 总和 (SUM)
    4: 平均值 (AVG)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            numeric_data = func(*args, **kwargs)
            results = {}
            if 1 in operations:
                results['max'] = max(numeric_data) if numeric_data else None
            if 2 in operations:
                results['min'] = min(numeric_data) if numeric_data else None
            if 3 in operations:
                results['sum'] = sum(numeric_data) if numeric_data else 0
            if 4 in operations:
                results['avg'] = (sum(numeric_data) / len(numeric_data)) if numeric_data else None
            return results
        return wrapper
    return decorator


def DataGenerator(**config):
    """
    数据生成器函数，根据配置生成不同类型的数据
    支持的数据类型：整数、浮点数、字符串、字典、列表和元组
    """
    count = config.get('num', 1)
    results = []

    for _ in range(count):
        current_sample = []
        for data_type, settings in config.items():
            if data_type == 'num':
                continue
            if data_type == "integer":
                start, end = settings['range']
                current_sample.append(random.randint(start, end))
            elif data_type == "float":
                start, end = settings['range']
                current_sample.append(random.uniform(start, end))
            elif data_type == "string":
                chars = settings['characters']
                length = settings['length']
                current_sample.append(''.join(random.choices(chars, k=length)))
            elif data_type == "dictionary":
                key = ''.join(random.choices(string.ascii_letters, k=3))
                value = random.randint(0, 100)
                current_sample.append({key: value})
            elif data_type in ("list", "tuple"):
                nested_data = DataGenerator(**settings)
                current_sample.append(nested_data if data_type == "list" else tuple(nested_data))
        results.append(current_sample if len(current_sample) > 1 else current_sample[0])
    return results[0] if count == 1 else results


def print_xml_tree(element, level=0):
    """
    递归打印 XML 元素树
    """
    indent = "  " * level
    tag = element.tag
    if '}' in tag:
        tag = tag.split('}')[1]
    attributes = " ".join([f"{k}='{v}'" for k, v in element.attrib.items()])
    if attributes:
        print(f"{indent}<{tag} {attributes}>")
    else:
        print(f"{indent}<{tag}>")

    if element.text and element.text.strip():
        print(f"{indent}  {element.text.strip()}")

    for child in element:
        print_xml_tree(child, level + 1)

    print(f"{indent}</{tag}>")


def print_xml_file(file_path):
    """
    打印 XML 文件的数据树
    """
    try:
        parser = etree.XMLParser(recover=True, encoding='utf-8')
        with open(file_path, 'rb') as f:
            tree = etree.parse(f, parser)
        root = tree.getroot()

        if root.getparent() is None:
            if root.tag == etree.Comment:
                pass
            else:
                print_xml_tree(root)
            for sibling in root.itersiblings():
                print_xml_tree(sibling)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
    except etree.XMLSyntaxError as e:
        print(f"XML 语法错误：{e}")
    except Exception as e:
        print(f"解析 XML 文件时出错：{e}")


def extract_elements(file_name, elem_tag):
    """
    提取 XML 文件中的特定元素
    """
    def dealwithElement(elem):
        if hasattr(elem, 'text') and elem.text:
            print(elem.text)

    class XMLExtractor:
        def __init__(self):
            self.count = 0

        def parse(self, file_name, elem_tag, callback):
            self.count = 0
            context = etree.iterparse(file_name, tag=elem_tag, recover=True)
            for _, elem in context:
                callback(elem)
                self.count += 1
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
            return self.count

    extractor = XMLExtractor()
    count = extractor.parse(file_name, elem_tag, dealwithElement)
    print(f"已解析 {count} 个 XML 元素。")


if __name__ == "__main__":
    # 示例数据结构配置
    data_config = {
        'num': 5,
        "integer": {"range": (0, 100)},
        "float": {"range": (0, 100.0)},
        "string": {
            "characters": string.ascii_uppercase,
            "length": 5
        },
        "dictionary": {},
        "list": {
            "integer": {"range": (0, 10)},
            "float": {"range": (0, 1.0)}
        }
    }
    requested_stats = {2, 4}  # 请求最小值和平均值

    @StatisticsManager(*requested_stats)
    def generate_and_analyze(**settings):
        generated_data = DataGenerator(**settings)
        def extract_numerics(items):
            for item in items:
                if isinstance(item, (list, tuple)):
                    yield from extract_numerics(item)
                elif isinstance(item, dict):
                    yield from extract_numerics(item.values())
                elif isinstance(item, (int, float)):
                    yield item
        return list(extract_numerics([generated_data]))

    # 生成示例数据并进行统计分析
    example_data = DataGenerator(**data_config)
    print("生成的数据示例:", example_data)
    statistical_results = generate_and_analyze(**data_config)
    print("统计结果:", statistical_results)

    # 命令行参数解析
    parser = argparse.ArgumentParser(description='XML 文件工具')
    parser.add_argument('--file', help='XML 文件的路径')
    parser.add_argument('--tag', help='要提取的元素标签')
    parser.add_argument('--tree', action='store_true', help='打印 XML 文件的数据树')
    args = parser.parse_args()

    if args.file:
        if args.tree:
            print_xml_file(args.file)
        elif args.tag:
            extract_elements(args.file, args.tag)
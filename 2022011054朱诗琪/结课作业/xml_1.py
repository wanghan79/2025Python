#!/usr/bin/env python
# coding:utf-8
"""
XML大文件处理器 - 可处理超过500MB的XML文件
使用装饰器模式和迭代解析提高内存效率
输出指定标签的key,type，并统计文件中该标签的数量。
需要在终端调用
"""

import sys
from lxml import etree
from os import path
from functools import wraps
from collections import defaultdict
from optparse import OptionParser


class XMLProcessor:
    """
    使用装饰器模式处理大型XML文件的核心类
    """

    def __init__(self, element_handler=None):
        self.element_handler = element_handler
        if element_handler:
            wraps(element_handler)(self)

    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)

    def parse(self, file_path, target_tag, **kwargs):
        """
        解析XML文件的主要方法
        """
        self._validate_file(file_path)

        namespace = self._get_namespace(file_path)
        full_tag = f"{{{namespace}}}{target_tag}" if namespace else target_tag

        stats = defaultdict(int)
        context = etree.iterparse(file_path, events=('end',), tag=full_tag)

        try:
            for event, element in context:
                try:
                    if self.element_handler:
                        result = self.element_handler(element, stats=stats, **kwargs)
                        if result:  # 如果处理器返回结果则收集
                            stats['processed_results'] = stats.get('processed_results', [])
                            stats['processed_results'].append(result)
                finally:
                    element.clear()
                    stats['total_count'] += 1
                    # 清除已处理的上级节点
                    while element.getprevious() is not None:
                        del element.getparent()[0]
        except Exception as e:
            raise RuntimeError(f"XML解析错误: {e}")
        finally:
            del context

        return stats

    def _validate_file(self, file_path):
        """验证输入文件"""
        if not path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        if not file_path.lower().endswith('.xml'):
            raise ValueError("输入文件必须是XML格式")

    def _get_namespace(self, file_path):
        """获取XML命名空间"""
        try:
            for _, (prefix, uri) in etree.iterparse(file_path, events=('start-ns',)):
                return uri
            return ""
        except etree.XMLSyntaxError:
            return ""


def element_printer(element, stats, print_content=False, **kwargs):
    """默认元素处理器：打印元素结构"""
    tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
    stats[tag] += 1

    if print_content:
        print(f"\n<{tag}>")
        if element.text and element.text.strip():
            print(f"  Content: {element.text.strip()}")
        for attr, value in element.attrib.items():
            print(f"  @{attr}: {value}")
    return {'tag': tag, 'attrs': element.attrib}


def setup_cli_options():
    """配置命令行选项"""
    usage = "用法: %prog [选项] XML文件"
    parser = OptionParser(usage=usage)

    parser.add_option("-t", "--tag", dest="target_tag",
                      help="需要解析的XML标签名", metavar="TAG")
    parser.add_option("-p", "--print", action="store_true", dest="verbose",
                      default=False, help="打印元素内容")
    parser.add_option("-s", "--stats", action="store_true", dest="show_stats",
                      default=False, help="显示统计信息")
    parser.add_option("-o", "--output", dest="output_file",
                      help="输出结果到文件", metavar="FILE")

    return parser


def main():
    # 配置命令行界面
    parser = setup_cli_options()
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("请指定一个XML文件")

    xml_file = path.normpath(args[0])

    try:
        # 创建处理器实例（使用装饰器模式）
        processor = XMLProcessor(element_printer)

        # 解析XML文件
        results = processor.parse(
            xml_file,
            target_tag=options.target_tag,
            print_content=options.verbose
        )

        # 输出结果
        if options.show_stats:
            print("\n==== XML解析统计 ====")
            print(f"总处理元素数: {results['total_count']}")
            for tag, count in sorted(results.items()):
                if tag not in ['total_count', 'processed_results']:
                    print(f"{tag}: {count}")

        if options.output_file:
            with open(options.output_file, 'w') as f:
                f.write(f"处理完成，共解析 {results['total_count']} 个元素\n")
                if 'processed_results' in results:
                    f.write("处理结果:\n")
                    for item in results['processed_results']:
                        f.write(f"{item}\n")

        print(f"成功处理 {results['total_count']} 个 <{options.target_tag}> 元素")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
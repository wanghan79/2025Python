#!/usr/bin/env python
# coding:utf-8
import sys
from lxml import etree
import os
from functools import wraps


class XMLTagExtractor:

    def __init__(self):
        self.namespace_map = {}
        self.all_tags = set()

    def extract_tags(self, file_path):

        try:
            # 路径验证
            file_path = os.path.abspath(file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在：{file_path}")
            if not file_path.lower().endswith('.xml'):
                raise ValueError("仅支持.xml格式文件")

            # 流式解析配置
            context = etree.iterparse(
                file_path,
                events=('start',),
                huge_tree=True,
                remove_blank_text=True
            )

            # 解析过程
            for event, elem in context:
                try:
                    # 记录标签（包含命名空间）
                    self.all_tags.add(elem.tag)
                finally:
                    # 改进的内存清理逻辑
                    self._safe_element_cleanup(elem)

            # 解析命名空间映射
            self._parse_namespaces(file_path)

            return self.all_tags

        except Exception as e:
            print(f"解析失败：{str(e)}", file=sys.stderr)
            return set()
        finally:
            if 'context' in locals():
                del context

    def _safe_element_cleanup(self, elem):

        try:
            parent = elem.getparent()
            if parent is not None and len(parent) > 0:
                while len(parent) > 3:
                    parent.remove(parent[0])
        except Exception as e:
            print(f"元素清理警告：{str(e)}", file=sys.stderr)

    def _parse_namespaces(self, file_path):

        try:
            context = etree.iterparse(
                file_path,
                events=('start-ns',),
                huge_tree=True
            )

            for event, ns in context:
                prefix, uri = ns
                self.namespace_map[prefix] = uri

        except Exception as e:
            print(f"命名空间解析警告：{str(e)}", file=sys.stderr)

    def format_tags(self, tags_set):

        formatted = []
        for tag in sorted(tags_set):
            if '}' in tag:
                ns_uri, local_name = tag[1:].split('}', 1)
                prefix = [k for k, v in self.namespace_map.items() if v == ns_uri]
                prefix = prefix[0] if prefix else ns_uri
                formatted.append(f"{prefix}:{local_name}")
            else:
                formatted.append(tag)
        return formatted


def xml_parser_decorator(file_path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 初始化提取器
            extractor = XMLTagExtractor()

            # 执行标签提取
            all_tags = extractor.extract_tags(file_path)

            if all_tags:
                # 格式化输出结果
                formatted_tags = extractor.format_tags(all_tags)

                # 将结果添加到kwargs中
                kwargs['xml_tags'] = {
                    'count': len(formatted_tags),
                    'tags': formatted_tags
                }

            # 调用原始函数
            return func(*args, **kwargs)

        return wrapper

    return decorator




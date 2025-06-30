#!/usr/bin/env python
# coding:utf-8
"""
XML标签提取工具（修复版）
作者：李震康（基于原代码改进）
日期：2025-06-03
功能：稳定提取XML文件中的所有唯一标签（包含命名空间）
"""

import sys  # 修复：添加缺失的sys模块导入
from lxml import etree
import os


class XMLTagExtractor:
    """XML标签提取器（支持大文件和命名空间）"""

    def __init__(self):
        self.namespace_map = {}
        self.all_tags = set()

    def extract_tags(self, file_path):
        """
        提取XML文件中的所有唯一标签
        :param file_path: XML文件路径
        :return: 包含所有唯一标签的集合（格式：{namespace}localname）
        """
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
                events=('start',),  # 捕获所有开始事件
                huge_tree=True,  # 允许处理超大文件
                remove_blank_text=True
            )

            # 解析过程
            for event, elem in context:
                try:
                    # 记录标签（包含命名空间）
                    self.all_tags.add(elem.tag)

                finally:
                    # 改进的内存清理逻辑（避免NoneType错误）
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
        """安全的元素清理逻辑（修复NoneType错误）"""
        try:
            # 仅当存在父元素且不是根元素时执行清理
            parent = elem.getparent()
            if parent is not None and len(parent) > 0:
                # 保留最近3个元素防止过度清理
                while len(parent) > 3:
                    parent.remove(parent[0])
        except Exception as e:
            print(f"元素清理警告：{str(e)}", file=sys.stderr)

    def _parse_namespaces(self, file_path):
        """解析XML文件中的命名空间映射"""
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
        """格式化标签输出（添加命名空间前缀）"""
        formatted = []
        for tag in sorted(tags_set):
            # 解析带命名空间的标签
            if '}' in tag:
                ns_uri, local_name = tag[1:].split('}', 1)
                # 查找对应的命名空间前缀
                prefix = [k for k, v in self.namespace_map.items() if v == ns_uri]
                prefix = prefix[0] if prefix else ns_uri
                formatted.append(f"{prefix}:{local_name}")
            else:
                formatted.append(tag)
        return formatted


if __name__ == "__main__":
    # 配置参数
    XML_FILE_PATH = r"C:\Users\李震康\Desktop\案例分析3 large XML parser\案例分析3 large XML parser\P00734.xml"

    # 初始化提取器
    extractor = XMLTagExtractor()

    # 执行标签提取
    all_tags = extractor.extract_tags(XML_FILE_PATH)

    if all_tags:
        # 格式化输出结果
        formatted_tags = extractor.format_tags(all_tags)

        print(f"在文件中发现 {len(formatted_tags)} 个唯一标签：\n")
        for idx, tag in enumerate(formatted_tags, 1):
            print(f"{idx:03d}. {tag}")

        # 保存到文件（修复缩进）
        with open("tags_list.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_tags))
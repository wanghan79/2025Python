#!/usr/bin/env python
# coding:utf-8

"""
大型XML文件解析与树形结构构建工具

模块功能：
1. 提供了大型XML文件的内存友好解析器核心实现，支持处理超过500M的XML文件而不会内存溢出。
2. 提供了装饰器模式的接口，允许用户通过装饰器语法修饰处理函数，简化XML解析流程。
3. 构建无重复标签的层次树结构，自动合并相同标签节点，从根节点到叶节点形成完整的XML结构树。
4. 提供详细的XML结构统计分析，包括层次深度、标签关系、元素计数等多维度信息。
5. 支持指定目标标签解析或全量解析，适用于生物信息学数据处理和大规模XML文档分析场景。

作者：多雅晗
"""

import os
import sys
from lxml import etree
from os import path
from collections import defaultdict

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')


class XMLTreeNode:
    """XML树节点"""

    def __init__(self, tag, text=None, level=0):
        self.tag = tag
        self.text = text.strip() if text and text.strip() else None
        self.level = level
        self.children = {}  # 使用字典避免重复tag
        self.parent = None
        self.path = ""

    def add_child(self, child):
        """添加子节点，重复tag会被合并"""
        if child.tag in self.children:
            existing = self.children[child.tag]
            if child.text and child.text != existing.text:
                if existing.text:
                    existing.text += "; " + child.text
                else:
                    existing.text = child.text
            # 合并子节点
            for grandchild_tag, grandchild in child.children.items():
                existing.add_child(grandchild)
        else:
            self.children[child.tag] = child
            child.parent = self
            child.path = f"{self.path}/{child.tag}" if self.path else child.tag

    def print_tree(self, indent=0):
        """打印树结构"""
        prefix = "  " * indent
        text_info = f" (text: {self.text})" if self.text else ""
        print(f"{prefix}{self.tag} [Level: {self.level}]{text_info}")
        for child in self.children.values():
            child.print_tree(indent + 1)


class largeXMLDealer:
    """改装后的largeXMLDealer装饰器类"""

    def __init__(self, fileName, elemTag=None):
        """
        初始化装饰器
        Args:
            fileName: XML文件名
            elemTag: 目标元素标签，如果为None则处理所有元素
        """
        self.fileName = fileName
        self.elemTag = elemTag
        self.root_node = None
        self.tag_hierarchy = defaultdict(set)
        self.element_count = 0
        self.max_level = 0

    def __call__(self, func4Element):
        """装饰器调用方法"""

        def wrapper():
            print(f"开始解析XML文件: {self.fileName}")
            print(f"目标标签: {self.elemTag if self.elemTag else '所有标签'}")
            print("-" * 50)

            # 执行解析
            count = self.parse(self.fileName, self.elemTag, func4Element)

            # 输出统计信息
            self._print_statistics()

            print(f"Already parsed {count} XML elements.")
            return self.root_node

        return wrapper

    def parse(self, fileName, elemTag, func4Element=None):
        """解析XML文件"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError(f"文件不存在或不是XML文件: {fileName}")

        count = 0
        ns = self._getNamespace(fileName)
        ns_prefix = f"{{{ns}}}" if ns else ""

        # 构建完整的目标标签
        full_target_tag = f"{ns_prefix}{elemTag}" if elemTag else None

        try:
            # 使用start和end事件来构建树
            context = etree.iterparse(fileName, events=('start', 'end'))
            node_stack = []

            for event, elem in context:
                clean_tag = elem.tag.replace(ns_prefix, '') if ns_prefix else elem.tag
                current_level = len(node_stack)

                if event == 'start':
                    # 创建节点
                    node = XMLTreeNode(clean_tag, level=current_level)
                    node_stack.append(node)
                    self.max_level = max(self.max_level, current_level)

                    # 记录层次关系
                    if len(node_stack) > 1:
                        parent_tag = node_stack[-2].tag
                        self.tag_hierarchy[parent_tag].add(clean_tag)

                elif event == 'end':
                    if node_stack:
                        current_node = node_stack.pop()

                        # 设置文本
                        if elem.text and elem.text.strip():
                            current_node.text = elem.text.strip()

                        # 如果是目标标签或处理所有标签
                        if not full_target_tag or elem.tag == full_target_tag:
                            count += 1
                            self.element_count += 1

                            # 调用处理函数
                            if func4Element:
                                try:
                                    # 创建兼容的元素对象
                                    class CompatElement:
                                        def __init__(self, node, elem):
                                            self.tag = node.tag
                                            self.text = node.text
                                            self.level = node.level
                                            self.path = node.path
                                            self.attrib = dict(elem.attrib) if elem.attrib else {}

                                    compat_elem = CompatElement(current_node, elem)
                                    func4Element(compat_elem)
                                except Exception as e:
                                    print(f"处理元素时出错: {e}")

                        # 构建树结构
                        if node_stack:
                            parent_node = node_stack[-1]
                            parent_node.add_child(current_node)
                        else:
                            # 根节点
                            if self.root_node is None:
                                self.root_node = current_node
                            else:
                                # 合并多个根节点
                                if self.root_node.tag != "document":
                                    temp_root = XMLTreeNode("document", level=-1)
                                    temp_root.add_child(self.root_node)
                                    self.root_node = temp_root
                                self.root_node.add_child(current_node)

                        # 清理内存
                        elem.clear()
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]

            del context

        except Exception as e:
            print(f"解析XML时出错: {e}")
            raise e

        return count

    def _getNamespace(self, fileName):
        """获取XML命名空间"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError(f"文件不存在: {fileName}")

        result = ''
        try:
            context = etree.iterparse(fileName, events=('start-ns',))
            for event, elem in context:
                prefix, result = elem
                break
            del context
        except Exception:
            pass

        return result

    def _print_statistics(self):
        """打印统计信息"""
        print("\n" + "=" * 50)
        print("XML解析统计:")
        print(f"解析元素数量: {self.element_count}")
        print(f"最大层次深度: {self.max_level}")
        print(f"唯一标签数量: {len(self.tag_hierarchy)}")

        print("\n层次关系:")
        for parent, children in self.tag_hierarchy.items():
            print(f"  {parent} -> {', '.join(sorted(children))}")

        print("\n完整树结构:")
        if self.root_node:
            self.root_node.print_tree()
        print("=" * 50)


# 使用示例
if __name__ == "__main__":
    # 示例1: 处理accession标签
    @largeXMLDealer("P00734.xml", "accession")
    def dealwithElement_accession(elem):
        print(f"标签: {elem.tag}, 文本: {elem.text}, 层次: {elem.level}")


    # 示例2: 处理sequence标签
    @largeXMLDealer("P00734.xml", "sequence")
    def dealwithElement_sequence(elem):
        text_preview = elem.text[:50] + "..." if elem.text and len(elem.text) > 50 else elem.text
        print(f"序列标签: {elem.tag}, 文本预览: {text_preview}")


    # 示例3: 处理所有标签
    @largeXMLDealer("P00734.xml")
    def dealwithElement_all(elem):
        print(f"[L{elem.level}] {elem.tag}: {elem.text if elem.text else '(无文本)'}")


    # 根据命令行参数选择执行
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "accession":
            print("=== 处理accession标签 ===")
            dealwithElement_accession()
        elif mode == "sequence":
            print("=== 处理sequence标签 ===")
            dealwithElement_sequence()
        elif mode == "all":
            print("=== 处理所有标签 ===")
            dealwithElement_all()
        else:
            print("用法: python largeXMLDealer_decorator.py [accession|sequence|all]")
    else:
        print("默认执行accession模式")
        dealwithElement_accession()

"""
使用方法:
   python largeXMLDealer.py accession
   python largeXMLDealer.py sequence
   python largeXMLDealer.py all
"""
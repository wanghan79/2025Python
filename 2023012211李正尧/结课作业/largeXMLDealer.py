#!/usr/bin/env python
# coding:utf-8
import sys
import os
from lxml import etree
from collections import defaultdict
from optparse import OptionParser
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class XMLDealer:
    """类修饰器用于处理大型XML文件，解析指定标签的内容"""

    def __init__(self, fileName, elemTag):
        # 验证文件有效性
        if not os.path.isfile(fileName):
            raise FileNotFoundError(f"XML文件不存在: {fileName}")
        if not fileName.endswith(('.xml', '.XML')):
            raise ValueError(f"不是有效的XML文件: {fileName}")

        self.fileName = fileName
        self.elemTag = elemTag
        self.namespaces = self._getNamespaces(fileName)
        self.ns = {f"{{{ns}}}": ns for ns in self.namespaces}
        logging.info(f"正在处理文件: {fileName}, 解析标签: {elemTag}")

    def _getNamespaces(self, fileName):
        """获取XML文件的所有命名空间，处理无命名空间的情况"""
        namespaces = set()
        try:
            context = etree.iterparse(fileName, events=('start-ns',), load_dtd=True)
            for event, elem in context:
                prefix, ns = elem
                namespaces.add(ns)
        except Exception as e:
            logging.error(f"获取命名空间时出错: {e}")
        finally:
            if 'context' in locals():
                del context
        return namespaces

    def __call__(self, func):
        """修饰器核心逻辑，解析XML并调用元素处理函数"""

        def wrapper():
            count = 0
            try:
                # 构建完整标签（包含命名空间）
                for ns in self.ns:
                    full_tag = f"{ns}{self.elemTag}"
                    context = etree.iterparse(
                        self.fileName,
                        events=('end',),
                        tag=full_tag,
                        load_dtd=True
                    )

                    for event, elem in context:
                        try:
                            func(elem)  # 调用用户定义的元素处理函数
                        except Exception as e:
                            logging.error(f"处理元素时出错: {e}")
                        finally:
                            elem.clear()
                            # 清理兄弟节点以节省内存
                            while elem.getprevious() is not None:
                                del elem.getparent()[0]
                            count += 1

                logging.info(f"成功解析 {count} 个 {self.elemTag} 元素")
            except Exception as e:
                logging.error(f"解析过程中出错: {e}")
            finally:
                if 'context' in locals():
                    del context
            return count

        return wrapper

class XMLStructureAnalyzer:
    """分析XML文件的完整结构，包括层级关系和深度"""

    def __init__(self, fileName):
        # 验证文件有效性
        if not os.path.isfile(fileName):
            raise FileNotFoundError(f"XML文件不存在: {fileName}")
        if not fileName.endswith(('.xml', '.XML')):
            raise ValueError(f"不是有效的XML文件: {fileName}")

        self.fileName = fileName
        self.structure = defaultdict(set)  # 存储节点层级关系
        self.max_depth = 0  # 记录最大深度
        self.root_nodes = set()  # 存储根节点

    def analyze(self):
        """分析XML结构，构建节点层级关系"""
        try:
            context = etree.iterparse(
                self.fileName,
                events=('start', 'end'),
                load_dtd=True
            )

            current_path = []  # 记录当前路径
            depth = 0  # 当前深度

            for event, elem in context:
                if event == 'start':
                    depth += 1
                    # 处理命名空间，只保留标签名
                    tag = elem.tag.split('}')[-1]
                    current_path.append(tag)

                    # 构建当前路径字符串
                    path_str = '/'.join(current_path)

                    # 记录子节点关系
                    if len(current_path) > 1:
                        parent_path = '/'.join(current_path[:-1])
                        self.structure[parent_path].add(tag)

                    # 确定根节点
                    if depth == 1:
                        self.root_nodes.add(tag)

                    # 更新最大深度
                    if depth > self.max_depth:
                        self.max_depth = depth

                elif event == 'end':
                    depth -= 1
                    current_path.pop()

                # 清理元素以节省内存
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

            logging.info(f"成功分析XML结构，最大深度: {self.max_depth}")
        except Exception as e:
            logging.error(f"分析结构时出错: {e}")
        finally:
            if 'context' in locals():
                del context
        return self

    def print_structure(self):
        """以树形结构打印XML层级关系"""
        if not self.structure:
            logging.warning("未分析到XML结构，请先调用analyze()方法")
            return

        print("\n" + "=" * 60)
        print(f"XML结构分析结果 - 文件: {os.path.basename(self.fileName)}")
        print("=" * 60)

        # 打印根节点信息
        if self.root_nodes:
            print(f"\n发现 {len(self.root_nodes)} 个根节点:")
            for root in self.root_nodes:
                print(f"  - {root}")
                self._print_tree(root, 1)
        else:
            print("未找到明确的根节点")

        print(f"\n最大层级深度: {self.max_depth}")
        print("=" * 60 + "\n")

    def _print_tree(self, node, level):
        """递归打印树形结构"""
        indent = "  " * (level - 1)
        prefix = "├── " if level > 1 else ""
        print(f"{indent}{prefix}{node}")

        # 查找当前节点的所有子节点
        for parent_path, children in self.structure.items():
            if parent_path.endswith(node):
                for child in sorted(children):
                    self._print_tree(child, level + 1)

def parse_custom_xml(file_path, tag_name):
    """解析自定义XML文件的便捷函数"""
    try:
        # 使用类修饰器模式解析指定标签
        dealer = XMLDealer(file_path, tag_name)

        @dealer
        def element_handler(elem):
            """自定义元素处理函数，可根据需要修改"""
            if elem.text:
                print(elem.text.strip())  # 打印元素文本，去除前后空格

        element_handler()
    except Exception as e:
        logging.error(f"解析过程中出错: {e}")

def analyze_xml_structure(file_path):
    """分析XML结构的便捷函数"""
    try:
        analyzer = XMLStructureAnalyzer(file_path)
        analyzer.analyze().print_structure()
    except Exception as e:
        logging.error(f"分析结构时出错: {e}")

def main():
    """主函数，处理命令行参数"""
    usage = "usage: %prog [options] xml_file\n\n" + \
            "示例:\n" + \
            "  python script.py --parse accession myfile.xml\n" + \
            "  python script.py --analyze myfile.xml"

    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--parse", dest="parse_tag",
                      help="解析指定标签的内容，例如: accession")
    parser.add_option("-a", "--analyze", action="store_true", dest="analyze",
                      help="分析XML文件的完整结构")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("请指定一个XML文件")

    file_path = os.path.abspath(args[0])

    if not os.path.exists(file_path):
        parser.error(f"文件不存在: {file_path}")

    if options.analyze:
        # 分析XML结构
        analyze_xml_structure(file_path)
    elif options.parse_tag:
        # 解析指定标签
        parse_custom_xml(file_path, options.parse_tag)
    else:
        parser.print_help()
        parser.error("请指定 --analyze 或 --parse 选项")

if __name__ == "__main__":
    main()
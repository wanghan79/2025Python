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

# 自定义异常类，方便外部捕获
class FileNotFoundError(Exception):
    """文件不存在或不是有效的XML文件"""
    pass

class XMLFormatError(Exception):
    """XML格式错误"""
    pass

class XMLDealer:
    """类修饰器用于处理大型XML文件，解析指定标签的内容"""

    def __init__(self, fileName, elemTag):
        # 验证文件有效性
        if not os.path.isfile(fileName):
            raise FileNotFoundError(f"XML文件不存在: {fileName}")
        if not fileName.lower().endswith(('.xml', '.xml')):
            raise ValueError(f"不是有效的XML文件: {fileName}")

        self.fileName = fileName
        self.elemTag = elemTag
        self.namespaces = self._getNamespaces(fileName)
        self.ns = {f"{{{ns}}}": ns for ns in self.namespaces} if self.namespaces else {"": ""}
        logging.info(f"正在处理文件: {fileName}, 解析标签: {elemTag}")

    def _getNamespaces(self, fileName):
        """获取XML文件的所有命名空间，处理无命名空间的情况"""
        namespaces = set()
        try:
            # 尝试读取文件前几行，检查是否为有效XML
            with open(fileName, 'rb') as f:
                header = f.read(100).decode('utf-8', errors='ignore')
                if '<?xml' not in header:
                    logging.warning(f"文件可能不是有效的XML: {fileName}")
            
            context = etree.iterparse(fileName, events=('start-ns',))
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
                # 如果没有命名空间，尝试直接解析标签
                if not self.namespaces:
                    self._parse_tag(self.elemTag, func, count)
                else:
                    # 构建完整标签（包含命名空间）
                    for ns_prefix in self.ns:
                        full_tag = f"{ns_prefix}{self.elemTag}"
                        count += self._parse_tag(full_tag, func)
                
                logging.info(f"成功解析 {count} 个 {self.elemTag} 元素")
            except Exception as e:
                logging.error(f"解析过程中出错: {e}")
            return count

        return wrapper
    
    def _parse_tag(self, tag, func):
        """解析特定标签，返回处理的元素数量"""
        count = 0
        try:
            # 检查文件是否为空
            if os.path.getsize(self.fileName) == 0:
                logging.error(f"文件为空: {self.fileName}")
                return 0
                
            context = etree.iterparse(
                self.fileName,
                events=('end',),
                tag=tag,
                recover=True  # 尝试从错误中恢复
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
        except Exception as e:
            logging.error(f"解析标签 {tag} 时出错: {e}")
        finally:
            if 'context' in locals():
                del context
        return count

class XMLStructureAnalyzer:
    """分析XML文件的完整结构，包括层级关系和深度"""

    def __init__(self, fileName):
        # 验证文件有效性
        if not os.path.isfile(fileName):
            raise FileNotFoundError(f"XML文件不存在: {fileName}")
        if not fileName.lower().endswith(('.xml', '.xml')):
            raise ValueError(f"不是有效的XML文件: {fileName}")
            
        # 检查文件是否为空
        if os.path.getsize(fileName) == 0:
            raise XMLFormatError(f"文件为空: {fileName}")

        self.fileName = fileName
        self.structure = defaultdict(set)  # 存储节点层级关系
        self.max_depth = 0  # 记录最大深度
        self.root_nodes = set()  # 存储根节点
        self.element_counts = defaultdict(int)  # 统计各标签出现次数

    def analyze(self):
        """分析XML结构，构建节点层级关系"""
        try:
            # 尝试读取文件前几行，检查是否为有效XML
            with open(self.fileName, 'rb') as f:
                header = f.read(100).decode('utf-8', errors='ignore')
                if '<?xml' not in header:
                    logging.warning(f"文件可能不是有效的XML: {self.fileName}")
            
            context = etree.iterparse(
                self.fileName,
                events=('start', 'end'),
                recover=True  # 尝试从错误中恢复
            )

            current_path = []  # 记录当前路径
            depth = 0  # 当前深度

            for event, elem in context:
                if event == 'start':
                    depth += 1
                    # 处理命名空间，只保留标签名
                    tag = elem.tag.split('}')[-1]
                    current_path.append(tag)
                    self.element_counts[tag] += 1

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

    def print_structure(self, output=sys.stdout):
        """以树形结构打印XML层级关系"""
        if not self.structure:
            logging.warning("未分析到XML结构，请先调用analyze()方法")
            return

        print("\n" + "=" * 60, file=output)
        print(f"XML结构分析结果 - 文件: {os.path.basename(self.fileName)}", file=output)
        print("=" * 60, file=output)

        # 打印根节点信息
        if self.root_nodes:
            print(f"\n发现 {len(self.root_nodes)} 个根节点:", file=output)
            for root in sorted(self.root_nodes):
                print(f"  - {root}", file=output)
                self._print_tree(root, 1, output)
        else:
            print("未找到明确的根节点", file=output)

        print(f"\n最大层级深度: {self.max_depth}", file=output)
        
        # 打印标签统计
        print("\n标签统计 (前10个):", file=output)
        sorted_tags = sorted(self.element_counts.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags[:10]:
            print(f"  {tag}: {count}", file=output)
            
        print("=" * 60 + "\n", file=output)

    def _print_tree(self, node, level, output=sys.stdout):
        """递归打印树形结构"""
        indent = "  " * (level - 1)
        prefix = "├── " if level > 1 else ""
        print(f"{indent}{prefix}{node}", file=output)

        # 查找当前节点的所有子节点
        for parent_path, children in self.structure.items():
            if parent_path.endswith(node):
                for child in sorted(children):
                    self._print_tree(child, level + 1, output)

def create_sample_xml(file_path, content=None):
    """创建示例XML文件，用于测试"""
    if content is None:
        content = """<?xml version="1.0" encoding="UTF-8"?>
<uniprot xmlns="http://uniprot.org/uniprot">
  <entry>
    <accession>P00734</accession>
    <name>THRB_HUMAN</name>
    <protein>
      <recommendedName>
        <fullName>Prothrombin</fullName>
      </recommendedName>
    </protein>
    <organism>
      <name type="scientific">Homo sapiens</name>
    </organism>
    <feature type="DOMAIN">
      <description>Kringle 1</description>
    </feature>
  </entry>
</uniprot>
"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"已创建示例XML文件: {file_path}")
        return True
    except Exception as e:
        logging.error(f"创建示例文件时出错: {e}")
        return False

def parse_custom_xml(file_path, tag_name, output=sys.stdout):
    """解析自定义XML文件的便捷函数"""
    try:
        # 使用类修饰器模式解析指定标签
        dealer = XMLDealer(file_path, tag_name)

        @dealer
        def element_handler(elem):
            """自定义元素处理函数，可根据需要修改"""
            if elem.text and elem.text.strip():
                print(elem.text.strip(), file=output)  # 打印元素文本，去除前后空格

        return element_handler()
    except Exception as e:
        logging.error(f"解析过程中出错: {e}")
        return 0

def analyze_xml_structure(file_path, output=sys.stdout):
    """分析XML结构的便捷函数"""
    try:
        analyzer = XMLStructureAnalyzer(file_path)
        analyzer.analyze().print_structure(output)
        return True
    except Exception as e:
        logging.error(f"分析结构时出错: {e}")
        return False

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
    parser.add_option("-c", "--create", action="store_true", dest="create",
                      help="创建示例XML文件用于测试")

    (options, args) = parser.parse_args()

    if not args:
        parser.error("请指定一个XML文件")

    file_path = os.path.abspath(args[0])

    if options.create:
        create_sample_xml(file_path)
        return

    if not os.path.exists(file_path):
        parser.error(f"文件不存在: {file_path}")

    if options.analyze:
        # 分析XML结构
        analyze_xml_structure(file_path)
    elif options.parse_tag:
        # 解析指定标签
        count = parse_custom_xml(file_path, options.parse_tag)
        print(f"共解析 {count} 个 {options.parse_tag} 元素")
    else:
        parser.print_help()
        parser.error("请指定 --analyze 或 --parse 选项")

if __name__ == "__main__":
    main()
#!/usr/bin/env python
# coding:utf-8

import argparse
from lxml import etree
import re
from os import path


# 定义装饰器
def dealwithElementDecorator(func):
    def wrapper(elem):
        print(f"开始处理元素: {elem.tag}")
        try:
            result = func(elem)
            print(f"元素 {elem.tag} 处理完成")
            return result
        except Exception as e:
            print(f"处理元素 {elem.tag} 时出错: {e}")
    return wrapper


def print_xml_tree(element, level=0):
    """
    递归打印 XML 元素树
    :param element: 当前处理的 XML 元素
    :param level: 当前元素的层级
    """
    # 打印当前元素的标签和属性
    indent = "  " * level
    tag = element.tag
    # 移除命名空间前缀
    if '}' in tag:
        tag = tag.split('}')[1]
    attributes = " ".join([f"{k}='{v}'" for k, v in element.attrib.items()])
    if attributes:
        print(f"{indent}<{tag} {attributes}>")
    else:
        print(f"{indent}<{tag}>")

    # 打印元素的文本内容
    if element.text and element.text.strip():
        print(f"{indent}  {element.text.strip()}")

    # 递归处理子元素
    for child in element:
        print_xml_tree(child, level + 1)

    # 打印元素的结束标签
    print(f"{indent}</{tag}>")


def print_xml_file(file_path):
    """
    打印 XML 文件的数据树
    :param file_path: XML 文件的路径
    """
    try:
        # 解析 XML 文件
        parser = etree.XMLParser(recover=True, encoding='utf-8')
        with open(file_path, 'rb') as f:
            tree = etree.parse(f, parser)
        root = tree.getroot()

        # 处理森林情况，可能存在多个根元素
        if root.getparent() is None:
            if root.tag == etree.Comment:
                # 如果根是注释，跳过
                pass
            else:
                print_xml_tree(root)
            # 处理后续的兄弟元素
            for sibling in root.itersiblings():
                print_xml_tree(sibling)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
    except etree.XMLSyntaxError as e:
        print(f"XML 语法错误: {e}")
    except Exception as e:
        print(f"解析 XML 文件时出错: {e}")


class largeXMLDealer:
    """XML解析器，用于处理大型XML文件"""

    def __init__(self):
        """初始化解析器"""

    def parse(self, fileName, elemTag, func4Element=None):
        """
        解析大型XML文件
        
        参数:
            fileName: XML文件路径
            elemTag: 要处理的元素标签名
            func4Element: 处理每个元素的回调函数
        """
        if not path.isfile(fileName) or not fileName.endswith(('.xml', '.XML')):
            raise FileNotFoundError(f"文件不存在或不是XML文件: {fileName}")

        count = 0
        es = ('end',)

        # 获取命名空间
        ns = self._getNamespace(fileName)
        ns_uri = "{%s}" % ns if ns else ""

        # 尝试使用命名空间和不使用命名空间两种方式解析
        tags_to_try = [f"{ns_uri}{elemTag}", elemTag]

        try:
            # 先尝试带命名空间的标签
            context = etree.iterparse(fileName, events=es, tag=tags_to_try[0])

            for event, elem in context:
                try:
                    if func4Element:
                        func4Element(elem)
                except Exception as e:
                    print(f"处理元素时出错 (行 {elem.sourceline}): {e}")
                finally:
                    elem.clear()
                    count += 1
                    # 清理父节点中的引用，释放内存
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context

            if count == 0:
                # 如果没有找到带命名空间的标签，尝试不带命名空间的标签
                print("尝试使用不带命名空间的标签进行解析...")
                context = etree.iterparse(fileName, events=es, tag=tags_to_try[1])

                for event, elem in context:
                    try:
                        if func4Element:
                            func4Element(elem)
                    except Exception as e:
                        print(f"处理元素时出错 (行 {elem.sourceline}): {e}")
                    finally:
                        elem.clear()
                        count += 1
                        # 清理父节点中的引用，释放内存
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]
                del context

                if count > 0:
                    print(f"注意: 成功使用不带命名空间的标签解析了 {count} 个元素")

            return count

        except Exception as e:
            print(f"解析XML文件时出错: {e}")
            return 0

    def _getNamespace(self, fileName):
        """获取XML文件的默认命名空间"""
        try:
            # 只读取文件的前1000个字符来获取命名空间，避免加载整个文件
            with open(fileName, 'r', encoding='utf-8') as f:
                first_chunk = f.read(1000)
                # 简单的正则表达式匹配命名空间
                match = re.search(r'xmlns="(.*?)"', first_chunk)
                return match.group(1) if match else ''
        except Exception as e:
            print(f"获取命名空间失败: {e}")
            return ''


if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='打印 XML 文件的数据树')
    parser.add_argument('file_path', help='XML 文件的路径')
    parser.add_argument('elemTag', help='要解析的元素标签名')

    # 解析命令行参数
    args = parser.parse_args()

    # 使用命令行指定的文件路径
    file_path = args.file_path
    elemTag = args.elemTag


    # 定义元素处理函数（使用修饰器）
    @dealwithElementDecorator
    def dealwithElement(elem):
        """处理单个XML元素"""
        print_xml_tree(elem)


    # 创建XML解析器实例
    xml_parser = largeXMLDealer()

    # 执行解析
    try:
        count = xml_parser.parse(file_path, elemTag, dealwithElement)
        print(f"成功解析 {count} 个元素")
    except Exception as e:
        print(f"解析过程中发生错误: {e}")
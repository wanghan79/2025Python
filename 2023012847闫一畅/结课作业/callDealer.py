#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

import re  # 添加缺失的导入
from lxml import etree
from os import path, listdir
from optparse import OptionParser


# 定义修饰器
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


def main():
    """主函数"""
    # 提供完整的文件路径
    xml_file = r"D:\\桌面\\结课作业\\P00734.xml"
    target_tag = "entry"  # 要解析的标签名

    print(f"正在尝试查找文件: {xml_file}")

    # 检查文件是否存在
    if not path.isfile(xml_file):
        print("错误: 文件不存在!")

        # 尝试列出目录内容，辅助调试
        dir_path = path.dirname(xml_file)
        if path.isdir(dir_path):
            print("\n目录内容:")
            for item in listdir(dir_path):
                print(f"- {item}")
        return

    print(f"正在解析文件: {xml_file}")
    print(f"目标标签: {target_tag}")

    # 创建XML解析器实例
    xml_parser = largeXMLDealer()

    # 定义元素处理函数（使用修饰器）
    @dealwithElementDecorator
    def dealwithElement(elem):
        """处理单个XML元素"""
        if elem.text:
            print(f"{elem.tag}: {elem.text.strip()}")

        # 处理子元素
        for child in elem:
            child_tag = child.tag
            # 移除命名空间前缀
            if '}' in child_tag:
                child_tag = child_tag.split('}')[1]

            if child.text and child.text.strip():
                print(f"  {child_tag}: {child.text.strip()}")

    # 执行解析
    try:
        count = xml_parser.parse(xml_file, target_tag, dealwithElement)
        print(f"成功解析 {count} 个元素")
    except Exception as e:
        print(f"解析过程中发生错误: {e}")


if __name__ == "__main__":
    main()
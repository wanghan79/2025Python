#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

from lxml import etree
from os import path
from optparse import OptionParser

def xml_element_parser(func):
    """
    装饰器：用于解析指定标签的XML元素并逐个传递给处理函数
    """

    def wrapper(self, file_name, elem_tag, *args, **kwargs):
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError(f"Invalid XML file: {file_name}")

        count = 0
        ns = self._getNamespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""

        context = etree.iterparse(file_name, events=("end",), tag=ns_prefix + elem_tag)

        for event, elem in context:
            try:
                # 调用传入的处理函数
                func(self, elem, *args, **kwargs)
            except Exception as e:
                raise RuntimeError(f"Error in element processing function: {e}")
            finally:
                elem.clear()
                count += 1
                # 删除前面的兄弟节点以节省内存
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

        del context
        return count

    return wrapper

def xml_tree_parser(output_func):
    """
    装饰器：解析XML树状结构并传递给输出函数
    """

    def wrapper(self, file_name, root_tag=None, *args, **kwargs):
        # 验证文件有效性
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError(f"Invalid XML file: {file_name}")

        # 解析XML树结构
        tree_data = self._build_tree_structure(file_name, root_tag)

        # 调用输出函数
        output_func(tree_data, *args, **kwargs)

        return tree_data

    return wrapper


class largeXMLDealer:
    """

    """

    def _build_tree_structure(self, file_name, root_tag=None):
        """
        构建XML标签树状结构数据
        """
        ns = self._getNamespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""

        context = etree.iterparse(file_name, events=('start', 'end'))
        tree = {}
        path_stack = [tree]
        depth = 0

        for event, elem in context:
            if event == 'start':
                depth += 1
                current_tag = elem.tag.replace(ns_prefix, '')  # 移除命名空间前缀

                if depth == 1 and root_tag and current_tag != root_tag:
                    continue  # 跳过非目标根节点

                new_node = {}
                path_stack[-1][current_tag] = new_node
                path_stack.append(new_node)

            elif event == 'end':
                depth -= 1
                if depth > 0:
                    path_stack.pop()

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        del context
        return tree

    @xml_element_parser
    def process_accession(self, elem):
        print(elem.text)
    def parse(self, fileName, elemTag, func4Element=None):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            # Call the outside function to deal with the element here
            try:
                func4Element(elem)
            except Exception:
                raise Exception("Something wrong in function parameter: func4Element")
            finally:
                elem.clear()
                count = count + 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        # Return how many elements had been parsed
        return count

    def _getNamespace(self, fileName):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            # print("%s, %d"%(elem, len(elem)))
            break
        del context
        return result


    @xml_tree_parser
    def output_tree(tree_data, indent=0, is_last=True, prefix=""):
        """
        输出XML树状结构
        """

        def print_node(node, indent_level, is_last_child, current_prefix):
            items = list(node.items())
            for i, (tag, children) in enumerate(items):
                is_last = i == len(items) - 1

                # 打印当前节点
                if indent_level == 0:
                    print(tag)
                else:
                    connector = "└── " if is_last else "├── "
                    print(f"{current_prefix}{connector}{tag}")

                # 更新缩进前缀
                new_prefix = current_prefix
                if indent_level > 0:
                    new_prefix += "    " if is_last else "│   "

                # 递归打印子节点
                if children:
                    print_node(children, indent_level + 1, is_last, new_prefix)

        print_node(tree_data, 0, True, "")


def main():
    """
    
    """
    # Construct the usage.
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False, action="store_true",
                      help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile", default=None,
                      help="Output the results to a file.")
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                      help="The XML tag interested to parse.")
    # Parse the options and args input by users.
    (options, args) = parser.parse_args()

    # Check the correction of users input and call the fuctions of class DoSomething.
    if (len(args) != 1):
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not exist or a vailable XML file.")
    # Call XML parser
    largXML = largeXMLDealer()
    count = largXML.parse(filePath, options.tag)
    print("Parsed %10d XML elements." % count)


if __name__ == "__main__":
    # 在largeXMLDealer实例上调用
    parser = largeXMLDealer()

    # 解析并输出完整的XML树结构
    parser.output_tree("P00734.xml")  # type: ignore

    # 解析并输出特定根节点下的结构
    # parser.output_tree("P00734.xml", root_tag="gene")  # type: ignore

    # main()
# Linux Command Line Example:
# python largeXMLDealer.py -t entry /home/Biodata/OrignalData/Protein/Uniprot/current/uniprot_sprot.xml

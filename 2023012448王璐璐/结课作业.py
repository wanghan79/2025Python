#!/usr/bin/env python
# coding:utf-8
"""
大型XML文件处理器 - 支持高效解析和树状结构展示
功能：
1. 流式解析大型XML文件（>500MB）
2. 支持按标签提取和处理元素
3. 生成XML树状结构可视化
4. 自动处理命名空间
"""

import sys
from os import path
from lxml import etree

class XMLProcessor:
    """高效处理大型XML文件的处理器"""
    
    def __init__(self):
        self.namespace_cache = {}
    
    def parse_elements(self, file_name, elem_tag, process_func):
        """
        流式解析XML元素
        :param file_name: XML文件路径
        :param elem_tag: 要提取的元素标签
        :param process_func: 元素处理函数
        :return: 处理的元素数量
        """
        self._validate_xml_file(file_name)
        ns = self._get_namespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        
        count = 0
        context = etree.iterparse(file_name, events=("end",), tag=ns_prefix + elem_tag)
        
        for event, elem in context:
            try:
                process_func(elem)
            except Exception as e:
                raise RuntimeError(f"元素处理错误: {e}")
            finally:
                elem.clear()
                count += 1
                # 清除已处理的兄弟节点释放内存
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        
        del context
        return count

    def build_xml_tree(self, file_name, root_tag=None):
        """
        构建XML树状结构
        :param file_name: XML文件路径
        :param root_tag: 指定根标签（可选）
        :return: 树状结构字典
        """
        self._validate_xml_file(file_name)
        ns = self._get_namespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        
        context = etree.iterparse(file_name, events=('start', 'end'))
        tree = {}
        path_stack = [tree]
        current_depth = 0
        target_depth = 0
        
        for event, elem in context:
            tag = elem.tag.replace(ns_prefix, '')  # 移除命名空间前缀
            
            if event == 'start':
                current_depth += 1
                
                # 如果指定了根标签，则从根标签开始构建
                if root_tag and current_depth == 1 and tag != root_tag:
                    continue
                
                # 创建新节点
                new_node = {}
                
                # 处理多个相同子标签的情况
                if tag in path_stack[-1]:
                    if not isinstance(path_stack[-1][tag], list):
                        path_stack[-1][tag] = [path_stack[-1][tag]]
                    path_stack[-1][tag].append(new_node)
                else:
                    path_stack[-1][tag] = new_node
                
                path_stack.append(new_node)
                
                # 记录目标深度
                if root_tag and current_depth == 1:
                    target_depth = current_depth
                else:
                    target_depth = current_depth - 1 if root_tag else current_depth
            
            elif event == 'end':
                if current_depth > target_depth:
                    path_stack.pop()
                current_depth -= 1
            
            # 清理内存
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        
        del context
        return tree

    def print_tree(self, tree_data, indent=0, is_last=True, prefix=""):
        """
        打印XML树状结构
        :param tree_data: 树状结构数据
        :param indent: 缩进级别
        :param is_last: 是否是最后一个子节点
        :param prefix: 前缀字符串
        """
        if not tree_data:
            return
        
        items = list(tree_data.items())
        for i, (tag, children) in enumerate(items):
            is_last_child = i == len(items) - 1
            
            # 打印当前节点
            if indent == 0:
                print(tag)
            else:
                connector = "└── " if is_last_child else "├── "
                print(f"{prefix}{connector}{tag}")
            
            # 更新缩进前缀
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            # 递归打印子节点
            if isinstance(children, dict):
                self.print_tree(children, indent + 1, is_last_child, new_prefix)
            elif isinstance(children, list):
                for j, child in enumerate(children):
                    is_last_in_list = j == len(children) - 1
                    self.print_tree(child, indent + 1, is_last_in_list, new_prefix)

    def _validate_xml_file(self, file_name):
        """验证XML文件有效性"""
        if not path.isfile(file_name):
            raise FileNotFoundError(f"文件不存在: {file_name}")
        if not file_name.lower().endswith('.xml'):
            raise ValueError(f"非XML文件: {file_name}")

    def _get_namespace(self, file_name):
        """获取XML命名空间"""
        if file_name in self.namespace_cache:
            return self.namespace_cache[file_name]
        
        self._validate_xml_file(file_name)
        context = etree.iterparse(file_name, events=('start-ns',))
        
        namespace = ''
        for event, elem in context:
            if event == 'start-ns':
                namespace = elem[1]
                break
        
        del context
        self.namespace_cache[file_name] = namespace
        return namespace


# 示例处理函数
def print_element_text(elem):
    """打印元素文本内容"""
    print(elem.text)

def main():
    """命令行入口点"""
    if len(sys.argv) < 3:
        print("用法: python xml_processor.py <XML文件> <标签> [根标签]")
        print("示例:")
        print("  提取accession: python xml_processor.py P00734.xml accession")
        print("  提取sequence: python xml_processor.py P00734.xml sequence")
        print("  显示树结构: python xml_processor.py P00734.xml tree entry")
        sys.exit(1)
    
    file_name = sys.argv[1]
    elem_tag = sys.argv[2]
    root_tag = sys.argv[3] if len(sys.argv) > 3 else None
    
    processor = XMLProcessor()
    
    try:
        if elem_tag.lower() == "tree":
            if not root_tag:
                print("错误: 显示树结构需要指定根标签")
                sys.exit(1)
                
            tree_data = processor.build_xml_tree(file_name, root_tag)
            processor.print_tree(tree_data)
        else:
            print(f"正在处理 {file_name} 中的 <{elem_tag}> 元素...")
            count = processor.parse_elements(file_name, elem_tag, print_element_text)
            print(f"\n已处理 {count} 个元素")
    except Exception as e:
        print(f"处理错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

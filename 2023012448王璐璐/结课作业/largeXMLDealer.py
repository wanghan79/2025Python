#!/usr/bin/env python
# coding:utf-8
"""
largeXMLDealer.py - 大型XML处理器
功能：高效处理大型XML文件（>500MB）
"""

from lxml import etree
from os import path

class LargeXMLDealer:
    def _get_namespace(self, file_name):
        """获取XML文档的命名空间"""
        if not path.isfile(file_name) or not file_name.endswith(".xml"):
            raise FileNotFoundError("XML文件无效或不存在")
        
        context = etree.iterparse(file_name, events=("start-ns",))
        for event, elem in context:
            return elem[1]  # 返回命名空间URI
        return ''

    def process_accession(self, file_name):
        """处理accession元素"""
        if not path.isfile(file_name) or not file_name.endswith(".xml"):
            raise FileNotFoundError("XML文件无效或不存在")
        
        ns = self._get_namespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        context = etree.iterparse(file_name, events=("end",), tag=ns_prefix + "accession")
        
        count = 0
        for event, elem in context:
            try:
                print(f"Accession: {elem.text}")
            except Exception as e:
                print(f"处理错误: {e}")
            finally:
                elem.clear()
                count += 1
                # 清理前兄弟节点释放内存
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        
        del context
        return count

    def process_sequence(self, file_name):
        """处理sequence元素"""
        if not path.isfile(file_name) or not file_name.endswith(".xml"):
            raise FileNotFoundError("XML文件无效或不存在")
        
        ns = self._get_namespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        context = etree.iterparse(file_name, events=("end",), tag=ns_prefix + "sequence")
        
        count = 0
        for event, elem in context:
            try:
                print(f"Sequence: {elem.text.strip()}")
            except Exception as e:
                print(f"处理错误: {e}")
            finally:
                elem.clear()
                count += 1
                # 清理前兄弟节点释放内存
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        
        del context
        return count

    def process_feature(self, file_name):
        """处理feature元素"""
        if not path.isfile(file_name) or not file_name.endswith(".xml"):
            raise FileNotFoundError("XML文件无效或不存在")
        
        ns = self._get_namespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        context = etree.iterparse(file_name, events=("end",), tag=ns_prefix + "feature")
        
        count = 0
        for event, elem in context:
            try:
                feature_type = elem.get("type")
                location = elem.find(ns_prefix + "location")
                begin = location.find(ns_prefix + "begin").get("position")
                end = location.find(ns_prefix + "end").get("position")
                print(f"Feature: {feature_type} ({begin}-{end})")
            except Exception as e:
                print(f"处理错误: {e}")
            finally:
                elem.clear()
                count += 1
                # 清理前兄弟节点释放内存
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        
        del context
        return count

    def output_tree(self, file_name, root_tag=None):
        """输出XML树状结构"""
        if not path.isfile(file_name) or not file_name.endswith(".xml"):
            raise FileNotFoundError("XML文件无效或不存在")
        
        ns = self._get_namespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        context = etree.iterparse(file_name, events=("start", "end"))
        
        tree = {}
        path_stack = [tree]
        depth = 0

        for event, elem in context:
            if event == "start":
                depth += 1
                current_tag = elem.tag.replace(ns_prefix, "")
                
                # 如果指定了根标签且当前不是根标签则跳过
                if depth == 1 and root_tag and current_tag != root_tag:
                    continue
                
                new_node = {}
                path_stack[-1][current_tag] = new_node
                path_stack.append(new_node)
                
            elif event == "end":
                depth -= 1
                if depth > 0:
                    path_stack.pop()
                
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        
        del context
        self._print_tree(tree)
    
    def _print_tree(self, tree_data, indent=0, is_last=True, prefix=""):
        """打印树状结构（辅助函数）"""
        if not tree_data:
            return
        
        items = list(tree_data.items())
        for i, (tag, children) in enumerate(items):
            is_last_child = i == len(items) - 1
            
            # 打印当前节点
            if indent == 0:
                print(tag)
            else:
                symbol = "└── " if is_last_child else "├── "
                print(f"{prefix}{symbol}{tag}")
            
            # 递归打印子节点
            new_prefix = prefix + ("    " if is_last else "│   ")
            self._print_tree(children, indent + 1, is_last_child, new_prefix)
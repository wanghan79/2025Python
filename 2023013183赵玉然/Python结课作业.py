#!/usr/bin/env python
# coding:utf-8

import sys
from os import path
from functools import wraps
from lxml import etree

class XMLParser:
    def __init__(self):
        self.namespace = None
    def get_namespace(self, file_path):
        if not path.isfile(file_path) or not file_path.endswith("xml"):
            raise FileNotFoundError(f"XML文件未找到: {file_path}")
        
        context = etree.iterparse(file_path, events=('start-ns',))
        for event, elem in context:
            self.namespace = f"{{{elem[1]}}}" 
        del context
        return self.namespace

    def parse_decorator(self, elem_tag):
        def decorator(process_func):
            @wraps(process_func)
            def wrapper(file_path):
                if not self.namespace:
                    self.get_namespace(file_path)
                
                full_tag = f"{self.namespace}{elem_tag}" if self.namespace else elem_tag
                count = 0
                
                try:
                    context = etree.iterparse(file_path, events=('end',), tag=full_tag)
                    
                    for event, elem in context:
                        try:
                            process_func(elem)
                            count += 1
                        finally:
                            elem.clear()
                            while elem.getprevious() is not None:
                                del elem.getparent()[0]
                    
                    return count
                finally:
                    if 'context' in locals():
                        del context
            
            return wrapper
        return decorator

def main():
    if len(sys.argv) != 3:
        print("使用方法: python xml_decorator_parser.py <XML文件> <标签名>")
        print("示例:")
        print("  python xml_decorator_parser.py P00734.xml accession")
        print("  python xml_decorator_parser.py P00734.xml sequence")
        sys.exit(1)

    file_name = sys.argv[1]
    elem_tag = sys.argv[2]
    
    parser = XMLParser()
    def print_element_text(elem):
        if elem.text and elem.text.strip():
            print(elem.text.strip())
    
    try:
        @parser.parse_decorator(elem_tag)
        def process_elements(elem):
            print_element_text(elem)
        count = process_elements(file_name)
        print(f"共解析 {count} 个 {elem_tag} 元素")
        
    except FileNotFoundError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析过程中发生错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
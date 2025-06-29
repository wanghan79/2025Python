from functools import wraps
from lxml import etree
from largeXMLDealer import largeXMLDealer
import os
import sys
import time

def xml_analyzer():
    """XML解析装饰器工厂，动态接收文件路径和标签参数"""
    def decorator(target_function):
        @wraps(target_function)
        def executor(*args, **kwargs):
            file_path = kwargs.get('file_name')
            tag_name = kwargs.get('element_tag')
            output_destination = kwargs.get('output_file', None)
            
            if not os.path.isfile(file_path):
                print(f"错误: 文件 '{file_path}' 不存在")
                return
            
            xml_processor = largeXMLDealer()
            element_counter = 0

            def handle_element(current_element):
                nonlocal element_counter
                raw_tag = current_element.tag
                actual_tag = raw_tag.split('}', 1)[-1] if '}' in raw_tag else raw_tag
                
                if tag_name is None or actual_tag == tag_name:
                    element_counter += 1
                    try:
                        target_function(current_element, output_file=output_destination)
                    except Exception as e:
                        print(f"警告: 处理元素 <{actual_tag}> 时发生异常 - {str(e)}")
            
            start_time = time.time()
            file_size = os.path.getsize(file_path)
            size_in_mb = file_size / (1024 * 1024)
            print(f"开始解析XML文件: '{file_path}'")
            print(f"目标标签: '{tag_name if tag_name else '所有标签'}'")
            
            xml_processor.parse(file_path, handle_element)
            
            elapsed_time = time.time() - start_time
            processing_speed = size_in_mb / elapsed_time if elapsed_time > 0 else float('inf')
            
            print(f"\n解析操作完成！总计处理 {element_counter} 个元素")
        
        return executor
    return decorator

@xml_analyzer()
def handle_xml_element(element, output_file=None):
    if element.text and element.text.strip():
        content = element.text.strip()
        if output_file:
            output_file.write(content + "\n")
        else:
            print(content)

def display_usage_guide():
    print("使用说明:")
    print("  python callDealer.py <XML文件> <目标标签> [输出文件]")
    print("示例:")
    print("  python callDealer.py proteins.xml accession")
    print("  python callDealer.py taxonomy.xml taxon results.txt")
    print("说明:")
    print("  - XML文件: 需要解析的XML文件路径")
    print("  - 目标标签: 需要处理的XML元素标签")
    print("  - 输出文件: (可选) 结果输出的文件路径")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        display_usage_guide()
        sys.exit(1)
    
    xml_file = sys.argv[1]
    target_tag = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) >= 4 else None
    
    xml_file = os.path.abspath(xml_file)
    
    try:
        if output_path:
            output_path = os.path.abspath(output_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                print(f"解析结果将输出至: '{output_path}'")
                handle_xml_element(file_name=xml_file, element_tag=target_tag, output_file=f)
        else:
            handle_xml_element(file_name=xml_file, element_tag=target_tag)
            
    except Exception as e:
        print(f"XML解析过程中出现错误: {str(e)}")
        sys.exit(1)

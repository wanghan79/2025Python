
from functools import wraps
from lxml import etree
from largeXMLDealer import largeXMLDealer
import os
import sys

DEFAULT_FILE = os.path.join(os.path.dirname(__file__), "example.xml")
DEFAULT_TAG = 'sequence'

def xml_parser(file_name=DEFAULT_FILE, element_tag=DEFAULT_TAG):
    """
    XML解析装饰器工厂
    :param file_name: XML文件路径
    :param element_tag: 目标元素标签
    """
    def decorator(func_to_decorate):
        @wraps(func_to_decorate)
        def wrapper(*args, **kwargs):
            # 验证文件存在性
            if not os.path.isfile(file_name):
                print(f"错误: 文件 '{file_name}' 不存在")
                return
            
            # 创建XML处理器
            dealer = largeXMLDealer()
            
            # 定义元素处理回调
            def element_processor(elem):
                # 提取标签名（忽略命名空间）
                raw_tag = elem.tag
                tag_name = raw_tag.split('}', 1)[-1] if '}' in raw_tag else raw_tag
                
                # 检查标签匹配
                if element_tag is None or tag_name == element_tag:
                    try:
                        # 调用被装饰的函数处理元素
                        func_to_decorate(elem, *args, **kwargs)
                    except Exception as e:
                        print(f"警告: 处理元素 <{tag_name}> 时出错 - {str(e)}")
            
            # 开始解析XML
            print(f"开始解析XML文件: '{file_name}'")
            print(f"目标标签: '{element_tag if element_tag else '所有标签'}'")
            dealer.parse(file_name, element_processor)
            print(f"XML解析完成")
        
        return wrapper
    return decorator

@xml_parser(file_name=DEFAULT_FILE, element_tag=DEFAULT_TAG)
def process_element(elem, output_file=None):
    """
    元素处理函数
    :param elem: XML元素对象
    :param output_file: 输出文件对象
    """
    # 提取元素文本内容
    text = elem.text.strip() if elem.text and elem.text.strip() else ""
    
    # 输出结果
    if output_file:
        output_file.write(f"<{elem.tag.split('}', 1)[-1]}>\n")
        output_file.write(text + "\n\n")
    else:
        print(f"--- 元素: <{elem.tag.split('}', 1)[-1]}> ---")
        print(text)
        print("-----------------------\n")

if __name__ == "__main__":
    # 解析命令行参数
    args = sys.argv[1:]
    
    # 设置默认值
    xml_file = DEFAULT_FILE
    elem_tag = DEFAULT_TAG
    output_path = None
    
    # 处理命令行参数
    if len(args) >= 1:
        xml_file = args[0]
    if len(args) >= 2:
        elem_tag = args[1]
    if len(args) >= 3:
        output_path = args[2]
    
    # 执行XML处理
    try:
        if output_path:
            # 文件输出模式
            with open(output_path, 'w', encoding='utf-8') as f:
                print(f"结果将输出到: '{output_path}'")
                process_element(output_file=f)
        else:
            # 控制台输出模式
            process_element()
    except Exception as e:
        print(f"处理XML时发生错误: {str(e)}")
        sys.exit(1)

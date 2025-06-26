###################################################################################
##
##  Import
##
###################################################################################

from functools import wraps
from lxml import etree
from largeXMLDealer import largeXMLDealer
import os

###################################################################################
##
##  Constants
##
###################################################################################
fileName = os.path.join(os.path.dirname(__file__), "example.xml") # 请确保此路径对于您的环境是正确的
elemTag = 'sequence'  # None 表示处理所有标签

###################################################################################
##
##  Functions
##
###################################################################################

def largeXMLparse(file_name, element_tag):
    """
    一个装饰器，使用 largeXMLDealer 来解析XML文件。
    它根据 element_tag 筛选元素（如果提供了特定标签），并将匹配的元素传递给被修饰的函数。
    如果 element_tag 为 None，则处理所有元素。
    """
    def decorator(func_to_decorate):
        @wraps(func_to_decorate)
        def wrapper(*args, **kwargs):
            print(f"largeXMLparse: 已为文件 '{file_name}' 和标签 '{element_tag}' 初始化")
            dealer = largeXMLDealer()

            def element_processor_callback(elem):
                raw_elem_tag = elem.tag
                tag_name = raw_elem_tag
                if '}' in tag_name:
                    tag_name = tag_name.split('}', 1)[1]
                
                if element_tag is None or tag_name == element_tag:
                    print(f"  标签匹配 (条件: target_tag='{element_tag}', actual_raw_tag='{raw_elem_tag}', extracted_tag='{tag_name}')。正在调用被修饰的函数。")
                    func_to_decorate(elem, *args, **kwargs)

            dealer.parse(file_name, element_processor_callback)
        return wrapper
    return decorator


@largeXMLparse(file_name=fileName, element_tag=elemTag)
def output(elem):
    """
    此函数由 largeXMLparse 装饰器修饰。
    它接收一个XML元素，并打印该元素，同时保持其原有的层级结构。
    """
    print(f"--- 找到元素 ({elem.tag}) ---")
    try:
        print(etree.tostring(elem, pretty_print=True, encoding='unicode').strip())
    except Exception as e:
        print(f"将元素 {elem.tag if elem is not None else 'None'} 转换成字符串时出错: {e}")
    print("------------------------\n")

###################################################################################
##
##  Main
##
###################################################################################

if __name__ == "__main__":
    print(f"开始处理XML文件 '{fileName}'\n目标标签: '{elemTag}'\n")
    output()
    print("XML 处理完成。")

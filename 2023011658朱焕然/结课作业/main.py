import os
from functools import wraps
from lxml import etree
from largeXMLDealer import LargeXMLDealer

# === 基本配置 ===
file_name = os.path.join(os.path.dirname(__file__), "P00734.xml")
element_tag = 'sequence'  # None 表示所有元素都处理

# === 装饰器 ===
def large_xml_parse(file_name, element_tag=None):
    """
    装饰器：调用 LargeXMLDealer 解析大 XML
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[初始化] 文件: {file_name} | 标签: {element_tag}")
            dealer = LargeXMLDealer()

            def callback(elem):
                raw_tag = elem.tag
                pure_tag = raw_tag.split('}', 1)[1] if '}' in raw_tag else raw_tag

                if element_tag is None or pure_tag == element_tag:
                    print(f"[匹配] <{raw_tag}> → 调用用户函数")
                    func(elem, *args, **kwargs)

            dealer.parse(file_name, callback)
        return wrapper
    return decorator

# === 被修饰的回调 ===
@large_xml_parse(file_name=file_name, element_tag=element_tag)
def handle_element(elem):
    print(f"--- 元素: <{elem.tag}> ---")
    print(etree.tostring(elem, pretty_print=True, encoding='unicode').strip())
    print("--------------------------\n")

# === 入口 ===
if __name__ == "__main__":
    print(f"[开始] 解析: '{file_name}'\n")
    handle_element()
    print("[完成] XML 已全部处理！")

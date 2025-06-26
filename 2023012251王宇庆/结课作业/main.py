from functools import wraps
from lxml import etree
from LargeXMLParser import LargeXMLParser  # 确保该模块实现了 parse(file, callback)
import os

# 配置文件路径和标签
file_name = os.path.join(os.path.dirname(__file__), "example.xml")
target_tag = "sequence"  # 设置为 None 表示处理所有标签


def parse_large_xml(file_path, tag=None):
    """
    XML 文件解析装饰器工厂。
    参数:
        file_path: XML 文件路径
        tag: 要解析的标签名称（不含命名空间），为 None 时处理所有标签
    用法:
        @parse_large_xml("file.xml", "tag")
        def handle(elem):
            ...
    """
    def decorator(user_func):
        @wraps(user_func)
        def wrapper(*args, **kwargs):
            print(f"[解析器] 正在处理文件: '{file_path}'，目标标签: '{tag or '全部'}'")

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件未找到: {file_path}")

            parser = LargeXMLParser()

            def process_element(elem):
                # 提取无命名空间标签名
                full_tag = elem.tag
                plain_tag = full_tag.split('}', 1)[-1] if '}' in full_tag else full_tag

                if tag is None or plain_tag == tag:
                    print(f"  [匹配] <{plain_tag}>，正在调用处理函数...")
                    user_func(elem, *args, **kwargs)

            parser.parse(file_path, process_element)

        return wrapper
    return decorator


@parse_large_xml(file_path=file_name, tag=target_tag)
def handle_element(elem):
    """
    打印符合条件的 XML 元素内容
    """
    print(f"--- 发现元素 ({elem.tag}) ---")
    try:
        xml_str = etree.tostring(elem, pretty_print=True, encoding="unicode").strip()
        print(xml_str)
    except Exception as e:
        print(f"[错误] 无法打印元素内容: {e}")
    print("--------------------------\n")


if __name__ == "__main__":
    print("===== XML 解析启动 =====")
    handle_element()
    print("===== 解析完成 =====")

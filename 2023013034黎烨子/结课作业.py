import xml.etree.ElementTree as ET
import os
from functools import wraps


def create_test_xml(file_path):
    """创建绝对规范的测试XML文件"""
    if os.path.exists(file_path):
        os.remove(file_path)

    content = '''<?xml version="1.0" encoding="UTF-8"?>
<data>
    <item>
        <id>1</id>
        <name>测试1</name>
        <value>10.5</value>
    </item>
    <item>
        <id>2</id>
        <name>测试2</name>
        <value>20.3</value>
    </item>
</data>'''

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def xml_parser_decorator(file_path, chunk_size=1000):
    """XML大文件解析修饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not os.path.exists(file_path):
                print(f"创建测试文件 {file_path}...")
                create_test_xml(file_path)

            # 验证文件内容
            print("\n=== 文件前100字符 ===")
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f.read(100))
            print("===================")

            try:
                for event, elem in ET.iterparse(file_path, events=('start', 'end')):
                    if event == 'end' and elem.tag == 'item':
                        data = {child.tag: child.text for child in elem}
                        func([data], *args, **kwargs)  # 逐条处理
                        elem.clear()
                return True
            except ET.ParseError as e:
                raise ValueError(f"XML解析错误: {str(e)}\n文件路径: {os.path.abspath(file_path)}") from e

        return wrapper

    return decorator


if __name__ == "__main__":
    XML_FILE = 'test_data.xml'

    # 强制重新创建测试文件
    if os.path.exists(XML_FILE):
        os.remove(XML_FILE)


    @xml_parser_decorator(XML_FILE)
    def print_xml_data(data_chunk, prefix="Data:"):
        print(f"\n{prefix} (共{len(data_chunk)}条)")
        for i, item in enumerate(data_chunk, 1):
            print(f"记录{i}: {item}")


    print("开始处理XML文件:")
    try:
        result = print_xml_data()
        print("\nXML文件处理完成")
    except Exception as e:
        print(f"\n处理失败: {str(e)}")

    # 显示最终文件内容
    print("\n=== 最终文件内容 ===")
    with open(XML_FILE, 'r', encoding='utf-8') as f:
        print(f.read())
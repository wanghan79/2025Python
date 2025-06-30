from functools import wraps
import xml.etree.ElementTree as ET
from typing import Callable, Any


def xml_file_parser(xml_path: str, chunk_size: int = 1000):
    def decorator(print_func: Callable[[Any], None]):
        @wraps(print_func)
        def wrapper(*args, **kwargs):
            try:
                # 使用迭代解析大XML文件
                context = ET.iterparse(xml_path, events=('start', 'end'))

                # 转换为迭代器
                context = iter(context)

                # 获取根元素
                event, root = next(context)

                print(f"开始解析XML文件: {xml_path}")
                print(f"根元素: {root.tag}")

                chunk = []
                count = 0

                for event, elem in context:
                    if event == 'end' and elem.tag == 'record':  # 假设我们处理的是<record>元素
                        # 解析元素数据
                        data = {
                            'tag': elem.tag,
                            'attrib': elem.attrib,
                            'text': elem.text,
                            'children': {child.tag: child.text for child in elem}
                        }

                        chunk.append(data)
                        count += 1

                        # 达到分块大小时处理一次
                        if len(chunk) >= chunk_size:
                            print_func(chunk, *args, **kwargs)
                            chunk = []
                            # 清除已处理的元素以节省内存
                            elem.clear()
                            if elem != root:
                                root.clear()

                # 处理剩余的记录
                if chunk:
                    print_func(chunk, *args, **kwargs)

                print(f"解析完成，共处理 {count} 条记录")

            except ET.ParseError as e:
                print(f"XML解析错误: {e}")
            except Exception as e:
                print(f"处理XML文件时发生错误: {e}")
            finally:
                if 'context' in locals():
                    del context

        return wrapper

    return decorator


# 使用示例
if __name__ == "__main__":
    # 定义被装饰的打印函数
    @xml_file_parser("large_data.xml")  # 替换为你的XML文件路径
    def print_xml_data(data_chunk: list, style: str = "default"):

        print(f"\n=== 打印数据块 ({style} 样式) ===")
        for i, record in enumerate(data_chunk, 1):
            print(f"记录 {i}:")
            print(f"  标签: {record['tag']}")
            if record['attrib']:
                print(f"  属性: {record['attrib']}")
            if record['text'] and record['text'].strip():
                print(f"  文本: {record['text'].strip()}")
            if record['children']:
                print("  子元素:")
                for tag, text in record['children'].items():
                    print(f"    {tag}: {text if text else '空'}")
        print("=== 结束数据块 ===\n")


    # 调用被装饰的函数
    print_xml_data(style="detailed")

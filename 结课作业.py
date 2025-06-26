import xml.etree.ElementTree as ET
from typing import Callable, Dict, List, Any, Optional
import functools


def parse_large_xml(file_path: str, item_tag: str) -> List[Dict[str, str]]:
    """
    解析大型 XML 文件，使用迭代器避免内存溢出

    Args:
        file_path: XML 文件路径
        item_tag: 需要提取的项目标签名

    Returns:
        包含所有项目数据的列表
    """
    items = []
    context = ET.iterparse(file_path, events=('start', 'end'))
    # 跳过根元素
    _, root = next(context)

    current_item = None
    for event, elem in context:
        if event == 'start' and elem.tag == item_tag:
            current_item = {}
        elif event == 'end' and elem.tag == item_tag:
            # 收集当前项目的所有子元素数据
            for child in elem:
                current_item[child.tag] = child.text
            items.append(current_item)
            # 清除元素以释放内存
            root.clear()

    return items


def xml_parser_decorator(xml_file: str, item_tag: str):
    """
    装饰器：将 XML 大文件解析工作与数据处理函数解耦

    Args:
        xml_file: XML 文件路径
        item_tag: 需要提取的项目标签名
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 解析 XML 文件
                data = parse_large_xml(xml_file, item_tag)
                # 调用被装饰的函数处理解析后的数据
                return func(data, *args, **kwargs)
            except Exception as e:
                print(f"解析 XML 文件时出错: {e}")
                return None

        return wrapper

    return decorator


# 使用装饰器修饰数据打印函数
@xml_parser_decorator(xml_file='large_data.xml', item_tag='book')
def print_xml_data(data: List[Dict[str, str]], limit: Optional[int] = None):
    """
    打印 XML 解析后的数据

    Args:
        data: 解析后的 XML 数据
        limit: 限制打印的记录数，None 表示不限制
    """
    if not data:
        print("没有找到数据")
        return

    print(f"找到 {len(data)} 条记录")
    display_data = data[:limit] if limit else data

    for i, item in enumerate(display_data, 1):
        print(f"\n记录 {i}:")
        for key, value in item.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    # 示例调用，打印前 5 条记录
    print_xml_data(limit=5)
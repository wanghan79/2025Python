import xml.etree.ElementTree as ET
from functools import wraps
import time


def xml_parser(file_path):
    """
    解析XML大文件并为打印函数提供数据的修饰器

    参数:
        file_path: XML文件的路径
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            print(f"开始解析XML文件: {file_path}")

            # 使用迭代方式解析大型XML文件，避免内存问题
            context = ET.iterparse(file_path, events=('start', 'end'))

            # 用于存储解析的数据
            parsed_data = []

            # 当前元素的路径
            current_path = []

            for event, elem in context:
                if event == 'start':
                    current_path.append(elem.tag)
                elif event == 'end':
                    # 根据需要处理元素数据
                    if len(current_path) == 2 and current_path[-1] == 'item':  # 示例：处理每个item元素
                        item_data = {
                            'id': elem.get('id'),
                            'name': elem.findtext('name', ''),
                            'value': elem.findtext('value', '')
                        }
                        parsed_data.append(item_data)

                    # 弹出当前路径的最后一个元素
                    if current_path:
                        current_path.pop()

                    # 清除元素以释放内存，但保留根元素
                    if current_path:
                        elem.clear()

            print(f"XML解析完成，耗时: {time.time() - start_time:.2f}秒")
            print(f"解析到{len(parsed_data)}个数据项")

            # 将解析的数据传递给被修饰的函数
            return func(parsed_data, *args, **kwargs)

        return wrapper

    return decorator


# 使用示例:
@xml_parser("large_data.xml")
def print_data(data, format_type="simple"):
    """打印XML解析出的数据"""
    if not data:
        print("没有数据可显示")
        return

    if format_type == "simple":
        for i, item in enumerate(data):
            print(f"项目 {i + 1}: ID={item.get('id')}, 名称={item.get('name')}, 值={item.get('value')}")
    elif format_type == "json":
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"未知的格式类型: {format_type}")


# 调用函数(会自动解析XML并打印数据)
print_data(format_type="json")

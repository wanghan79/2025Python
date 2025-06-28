from functools import wraps
from lxml import etree
from largeXMLDealer import largeXMLDealer
import os
import sys
import time


def xml_parser():
    """
    XML解析装饰器工厂
    动态接收文件路径和标签作为参数
    """

    def decorator(func_to_decorate):
        @wraps(func_to_decorate)
        def wrapper(*args, **kwargs):
            # 从kwargs获取参数
            file_name = kwargs.get('file_name')
            element_tag = kwargs.get('element_tag')
            output_file = kwargs.get('output_file', None)

            # 验证文件存在性
            if not os.path.isfile(file_name):
                print(f"错误: 文件 '{file_name}' 不存在")
                return

            # 创建XML处理器
            dealer = largeXMLDealer()

            # 计数器初始化
            element_count = 0

            # 定义元素处理回调
            def element_processor(elem):
                nonlocal element_count
                # 提取标签名（忽略命名空间）
                raw_tag = elem.tag
                tag_name = raw_tag.split('}', 1)[-1] if '}' in raw_tag else raw_tag

                # 检查标签匹配
                if element_tag is None or tag_name == element_tag:
                    element_count += 1
                    try:
                        # 调用被装饰的函数处理元素
                        func_to_decorate(elem, output_file=output_file)
                    except Exception as e:
                        print(f"警告: 处理元素 <{tag_name}> 时出错 - {str(e)}")

            # 开始解析XML
            start_time = time.time()
            file_size = os.path.getsize(file_name)
            size_mb = file_size / (1024 * 1024)
            print(f"开始解析XML文件: '{file_name}'")
            print(f"目标标签: '{element_tag if element_tag else '所有标签'}'")

            dealer.parse(file_name, element_processor)

            # 计算处理时间
            elapsed = time.time() - start_time
            speed = size_mb / elapsed if elapsed > 0 else float('inf')

            print(f"\n解析完成！共处理 {element_count} 个元素")

        return wrapper

    return decorator


@xml_parser()
def process_element(elem, output_file=None):
    """
    简洁的元素处理函数
    :param elem: XML元素对象
    :param output_file: 输出文件对象
    """
    # 提取元素文本内容 - 仅当有文本时处理
    if elem.text and elem.text.strip():
        text = elem.text.strip()

        # 输出结果
        if output_file:
            output_file.write(text + "\n")
        else:
            print(text)


def print_usage():
    """打印使用说明"""
    print("使用说明:")
    print("  python callDealer.py <XML文件> <目标标签> [输出文件]")
    print("示例:")
    print("  python callDealer.py proteins.xml accession")
    print("  python callDealer.py taxonomy.xml taxon results.txt")
    print("说明:")
    print("  - XML文件: 要解析的XML文件路径")
    print("  - 目标标签: 要处理的XML元素标签")
    print("  - 输出文件: (可选) 结果输出文件路径")


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    # 解析命令行参数
    xml_file = sys.argv[1]
    elem_tag = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) >= 4 else None

    # 处理文件路径
    xml_file = os.path.abspath(xml_file)

    # 执行XML处理
    try:
        if output_path:
            # 文件输出模式
            output_path = os.path.abspath(output_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                print(f"结果将输出到: '{output_path}'")
                process_element(file_name=xml_file, element_tag=elem_tag, output_file=f)
        else:
            # 控制台输出模式
            process_element(file_name=xml_file, element_tag=elem_tag)

    except Exception as e:
        print(f"处理XML时发生错误: {str(e)}")
        sys.exit(1)
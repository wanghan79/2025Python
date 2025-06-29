from functools import wraps
from lxml import etree
from large_XMLD import largeXMLDealer
import os
import sys
import time


def xml_parser_factory():
    """
    XML解析装饰器工厂
    动态接收文件路径和标签作为参数
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 从kwargs获取参数
            xml_file_path = kwargs.get('file_name')
            target_tag = kwargs.get('element_tag')
            output_file_path = kwargs.get('output_file', None)

            # 验证文件存在性
            if not os.path.isfile(xml_file_path):
                print(f"错误: 文件 '{xml_file_path}' 不存在")
                return

            # 创建XML处理器
            xml_processor = largeXMLDealer()

            # 计数器初始化
            element_counter = 0

            # 定义元素处理回调
            def element_handler(elem):
                nonlocal element_counter
                # 提取标签名（忽略命名空间）
                full_tag = elem.tag
                tag_name = full_tag.split('}', 1)[-1] if '}' in full_tag else full_tag

                # 检查标签匹配
                if target_tag is None or tag_name == target_tag:
                    element_counter += 1
                    try:
                        # 调用被装饰的函数处理元素
                        func(elem, output_file=output_file_path)
                    except Exception as e:
                        print(f"警告: 处理元素 <{tag_name}> 时出错 - {str(e)}")

            # 开始解析XML
            start_time = time.time()
            file_size_bytes = os.path.getsize(xml_file_path)
            file_size_mb = file_size_bytes / (1024 * 1024)
            print(f"开始解析XML文件: '{xml_file_path}'")
            print(f"目标标签: '{target_tag if target_tag else '所有标签'}'")

            xml_processor.parse(xml_file_path, element_handler)

            # 计算处理时间
            elapsed_time = time.time() - start_time
            processing_speed = file_size_mb / elapsed_time if elapsed_time > 0 else float('inf')

            print(f"\n解析完成！共处理 {element_counter} 个元素")

        return wrapper

    return decorator


@xml_parser_factory()
def handle_element(elem, output_file=None):
    """
    简洁的元素处理函数
    :param elem: XML元素对象
    :param output_file: 输出文件对象
    """
    # 提取元素文本内容 - 仅当有文本时处理
    if elem.text and elem.text.strip():
        element_text = elem.text.strip()

        # 输出结果
        if output_file:
            output_file.write(element_text + "\n")
        else:
            print(element_text)


def display_usage():
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
        display_usage()
        sys.exit(1)

    # 解析命令行参数
    input_xml_file = sys.argv[1]
    target_element_tag = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) >= 4 else None

    # 处理文件路径
    input_xml_file = os.path.abspath(input_xml_file)

    # 执行XML处理
    try:
        if output_file:
            # 文件输出模式
            output_file = os.path.abspath(output_file)
            with open(output_file, 'w', encoding='utf-8') as f:
                print(f"结果将输出到: '{output_file}'")
                handle_element(file_name=input_xml_file, element_tag=target_element_tag, output_file=f)
        else:
            # 控制台输出模式
            handle_element(file_name=input_xml_file, element_tag=target_element_tag)

    except Exception as e:
        print(f"处理XML时发生错误: {str(e)}")
        sys.exit(1)
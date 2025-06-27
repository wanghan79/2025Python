#!/usr/bin/env python3
import argparse
from lxml import etree
from pathlib import Path


def find_xml_namespace(file_path: str) -> str:
    """返回XML文件的默认命名空间"""
    try:
        # 只解析文件的前100KB以快速获取命名空间
        with open(file_path, 'rb') as f:
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(f, parser)
            root = tree.getroot()
            return root.nsmap.get(None, '')
    except Exception:
        return ''


def stream_process_xml(
        file_path: str,
        tag_name: str,
        callback: callable = None
) -> int:
    """
    流式处理大型XML文件，逐元素解析

    Args:
        file_path: XML文件路径
        tag_name: 需要处理的标签名
        callback: 处理每个元素的回调函数

    Returns:
        处理的元素数量
    """
    xml_path = Path(file_path)
    if not xml_path.is_file() or xml_path.suffix.lower() != '.xml':
        raise ValueError(f"文件不存在或不是有效的XML: {file_path}")

    namespace = find_xml_namespace(file_path)
    qualified_tag = f"{{{namespace}}}{tag_name}" if namespace else tag_name

    count = 0
    try:
        with open(file_path, 'rb') as f:
            # 使用iterparse进行流式解析
            context = etree.iterparse(f, events=('end',), tag=qualified_tag)

            for event, element in context:
                if callback:
                    callback(element)

                # 内存优化：清理已处理的元素
                element.clear()
                # 清理父节点中的兄弟节点以释放更多内存
                while element.getprevious() is not None:
                    del element.getparent()[0]

                count += 1

            # 释放解析器资源
            del context

    except Exception as e:
        print(f"解析错误: {str(e)}", file=sys.stderr)
        raise

    return count


def create_element_processor(output_path: str = None) -> callable:
    """创建元素处理器函数"""
    if output_path:
        output_file = Path(output_path)
        # 确保输出目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)

        def write_to_file(element: etree._Element) -> None:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(etree.tostring(element, encoding='unicode') + '\n')

        return write_to_file

    def print_to_console(element: etree._Element) -> None:
        print(etree.tostring(element, encoding='unicode'))

    return print_to_console


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='高效解析大型XML文件')
    parser.add_argument('xml_file', help='XML文件路径')
    parser.add_argument('-t', '--tag', required=True, help='目标XML标签')
    parser.add_argument('-o', '--output', help='输出文件路径')

    args = parser.parse_args()

    input_file = Path(args.xml_file)
    if not input_file.exists():
        parser.error(f"文件不存在: {args.xml_file}")

    try:
        processor = create_element_processor(args.output)
        count = stream_process_xml(args.xml_file, args.tag, processor)
        print(f"成功处理 {count} 个元素", file=sys.stderr)
    except Exception as e:
        print(f"执行失败: {str(e)}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
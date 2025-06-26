#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys
import os
import argparse
import logging
from typing import Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    """解析命令行参数，提供更友好的帮助信息"""
    parser = argparse.ArgumentParser(
        description="处理大型XML文件 - 解析特定标签或分析结构",
        usage="%(prog)s [options] xml_file",
        epilog="示例:\n  %(prog)s P00734.xml accession\n  %(prog)s big_data.xml --analyze"
    )

    parser.add_argument("xml_file", help="要处理的XML文件路径")
    parser.add_argument("elem_tag", nargs="?", default=None,
                        help="要解析的元素标签名，如: accession")
    parser.add_argument("--analyze", "-a", action="store_true",
                        help="分析XML文件的完整结构，而非解析特定标签")
    parser.add_argument("--output", "-o", default=None,
                        help="将结果输出到指定文件，而非控制台")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="显示详细处理信息")

    return parser.parse_args()

def setup_output(output_file: Optional[str]):
    """设置输出目标（控制台或文件）"""
    if output_file:
        try:
            f = open(output_file, "w", encoding="utf-8")
            logging.info(f"结果将输出到文件: {output_file}")
            return f
        except Exception as e:
            logging.error(f"无法打开输出文件: {e}")
            sys.exit(1)
    return sys.stdout

def parse_element(xml_file: str, elem_tag: str, output=sys.stdout, verbose=False):
    """解析XML文件中的特定标签"""
    if verbose:
        logging.info(f"开始解析标签: {elem_tag} in {xml_file}")

    try:
        dealer = largeXMLDealer.XMLDealer(xml_file, elem_tag)

        @dealer
        def dealwithElement(elem):
            """处理元素的函数，可根据需要自定义"""
            if elem.text and elem.text.strip():
                print(elem.text.strip(), file=output)

        dealwithElement()

    except largeXMLDealer.FileNotFoundError:
        logging.error(f"错误: 文件不存在或不是有效的XML: {xml_file}")
    except Exception as e:
        logging.error(f"解析过程中出错: {e}")

def analyze_structure(xml_file: str, output=sys.stdout, verbose=False):
    """分析XML文件的结构"""
    if verbose:
        logging.info(f"开始分析XML结构: {xml_file}")

    try:
        analyzer = largeXMLDealer.XMLStructureAnalyzer(xml_file)
        analyzer.analyze()
        analyzer.print_structure()

    except largeXMLDealer.FileNotFoundError:
        logging.error(f"错误: 文件不存在或不是有效的XML: {xml_file}")
    except Exception as e:
        logging.error(f"分析结构时出错: {e}")

def main():
    """主函数，协调各个功能模块"""
    args = parse_arguments()

    # 检查文件存在性
    if not os.path.isfile(args.xml_file):
        logging.error(f"错误: 文件不存在: {args.xml_file}")
        sys.exit(1)

    # 设置输出
    output = setup_output(args.output)

    try:
        if args.analyze:
            # 分析XML结构
            analyze_structure(args.xml_file, output, args.verbose)
        elif args.elem_tag:
            # 解析特定标签
            parse_element(args.xml_file, args.elem_tag, output, args.verbose)
        else:
            # 缺少必要参数
            logging.error("错误: 请指定要解析的标签或使用--analyze选项")
            sys.exit(1)

    finally:
        # 确保文件输出流被关闭
        if args.output and output != sys.stdout:
            output.close()

if __name__ == "__main__":
    main()
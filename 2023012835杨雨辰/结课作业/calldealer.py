#!/usr/bin/env python3
# 大型XML文件处理工具
# 支持标签内容提取和结构分析功能

import sys
import os
import argparse
import logging
from typing import TextIO, Optional

# 导入自定义XML处理库
try:
    from LargeXMLParser import (
        XMLDealer,
        XMLStructureAnalyzer,
        create_sample_xml,
        FileNotFoundError as XMLFileError
    )
except ImportError:
    print("依赖错误: 无法加载XML处理模块，请检查LargeXMLParser是否正确安装")
    sys.exit(1)

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


class XMLToolkit:
    """XML处理工具集，封装文件操作和处理逻辑"""

    def __init__(self, args):
        self.args = args
        self.output_stream = None

    def setup_environment(self):
        """准备执行环境：检查文件、设置输出"""
        self._validate_input_file()
        self.output_stream = self._setup_output()

    def _validate_input_file(self):
        """验证输入文件是否存在，必要时创建示例文件"""
        if not os.path.isfile(self.args.xml_file):
            if self.args.create:
                logging.info(f"创建示例XML: {self.args.xml_file}")
                if not create_sample_xml(self.args.xml_file):
                    raise RuntimeError("示例文件创建失败")
            else:
                raise FileNotFoundError(f"输入文件不存在: {self.args.xml_file}")

    def _setup_output(self) -> TextIO:
        """配置输出目标（控制台或文件）"""
        if self.args.output:
            try:
                return open(self.args.output, 'w', encoding='utf-8')
            except Exception as e:
                logging.error(f"输出文件打开失败: {e}")
                sys.exit(1)
        return sys.stdout

    def process_xml(self):
        """根据命令行参数处理XML文件"""
        try:
            if self.args.analyze:
                self._analyze_structure()
            elif self.args.tag_name:
                self._extract_tag_content()
            else:
                raise ValueError("请指定操作模式: 标签提取(-t)或结构分析(-a)")
        finally:
            self._cleanup()

    def _extract_tag_content(self):
        """从XML中提取指定标签的内容"""
        if self.args.verbose:
            logging.info(f"开始提取标签: {self.args.tag_name}")

        try:
            dealer = XMLDealer(self.args.xml_file, self.args.tag_name)

            @dealer
            def process_element(element):
                """处理单个XML元素"""
                # 处理元素文本内容
                if element.text and element.text.strip():
                    print(element.text.strip(), file=self.output_stream)
                else:
                    # 处理子元素
                    has_children = False
                    for child in element:
                        has_children = True
                        if child.text and child.text.strip():
                            # 处理命名空间
                            clean_tag = child.tag
                            if '}' in child.tag:
                                clean_tag = child.tag.split('}')[1]
                            print(f"{clean_tag}: {child.text.strip()}",
                                  file=self.output_stream)

                    # 处理属性
                    if not has_children and element.attrib:
                        for attr_key, attr_val in element.attrib.items():
                            print(f"@{attr_key}: {attr_val}",
                                  file=self.output_stream)

            # 执行解析并输出统计信息
            count = process_element()
            print(f"成功解析 {count} 个 <{self.args.tag_name}> 标签",
                  file=self.output_stream)

        except XMLFileError:
            logging.error(f"文件错误: {self.args.xml_file} 无效")
            sys.exit(1)
        except Exception as e:
            logging.error(f"解析错误: {e}")
            sys.exit(1)

    def _analyze_structure(self):
        """分析并显示XML文件的结构"""
        if self.args.verbose:
            logging.info(f"开始结构分析: {self.args.xml_file}")

        try:
            analyzer = XMLStructureAnalyzer(self.args.xml_file)
            analyzer.analyze().print_structure(self.output_stream)
        except XMLFileError:
            logging.error(f"文件错误: {self.args.xml_file} 无效")
            sys.exit(1)
        except Exception as e:
            logging.error(f"结构分析错误: {e}")
            sys.exit(1)

    def _cleanup(self):
        """清理资源"""
        if self.output_stream and self.output_stream != sys.stdout:
            self.output_stream.close()


def parse_command_line():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="XML文件处理工具 - 高效解析大型XML文档",
        usage="%(prog)s [选项] <XML文件> [标签名]",
        epilog="示例:\n"
               "  %(prog)s -a data.xml        # 分析XML结构\n"
               "  %(prog)s -t accession data.xml  # 提取accession标签"
    )

    # 位置参数
    parser.add_argument("xml_file", help="XML文件路径")
    parser.add_argument("tag_name", nargs="?", default=None,
                        help="要提取的标签名称")

    # 选项参数
    parser.add_argument("--analyze", "-a", action="store_true",
                        help="分析XML文件结构")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="输出文件路径")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="显示详细处理信息")
    parser.add_argument("--create", "-c", action="store_true",
                        help="文件不存在时创建示例文件")

    return parser.parse_args()


def main():
    """程序主入口"""
    try:
        # 解析命令行参数
        args = parse_command_line()

        # 创建并运行XML处理工具
        xml_tool = XMLToolkit(args)
        xml_tool.setup_environment()
        xml_tool.process_xml()

    except Exception as e:
        logging.error(f"程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
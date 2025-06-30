# main.py

from largeXMLDealer import XMLParserUtil
import argparse
import os
from lxml import etree 


DEFAULT_SAMPLE_XML_PATH = os.path.join(os.path.dirname(__file__), "P00734.xml")

# 用于统计成功处理并打印的元素数量
printed_element_counter = 0

def print_formatted_xml_node(xml_node_object):
 
    global printed_element_counter
    printed_element_counter += 1

    # 从可能包含命名空间的标签中提取纯标签名
    clean_node_tag = ""
    if '}' in xml_node_object.tag:
        clean_node_tag = xml_node_object.tag.split('}', 1)[1]
    else:
        clean_node_tag = xml_node_object.tag

    print(f"\n--- 捕获并呈现节点: <{clean_node_tag}> (计数: {printed_element_counter}) ---")
    try:
        # 将 lxml 元素对象转换为易读的漂亮打印XML字符串
        node_xml_string = etree.tostring(xml_node_object, pretty_print=True, encoding='unicode').strip()
        print(node_xml_string)
    except Exception as conv_err:
        print(f"提示: 无法将节点 '{clean_node_tag}' 转换为字符串形式进行展示: {conv_err}")
    print("---------------------------------------------")


def main():
    """
    主程序入口点，负责处理命令行参数，并启动XML解析过程。
    """
    cmd_parser = argparse.ArgumentParser(
        description="一个实用的Python脚本，用于对大型XML文档进行解析与内容过滤。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助文本格式
    )
    cmd_parser.add_argument(
        "xml_source_path",
        nargs='?', # 使路径参数成为可选，方便测试
        default=DEFAULT_SAMPLE_XML_PATH,
        help=f"指定要解析的XML文件的路径。\n默认为: {DEFAULT_SAMPLE_XML_PATH}"
    )
    cmd_parser.add_argument(
        "-f", "--filter_tag", # 改变了短参数和长参数名称
        default="sequence", # 默认仍然是sequence，以与你同学作业保持功能一致
        help="可选: 仅处理并显示匹配此XML标签的元素（不含命名空间）。\n例如: 'sequence'、'entry' 或 'accession'。\n如果未提供此参数，将显示所有被解析的元素。"
    )

    app_arguments = cmd_parser.parse_args()

    # 重置计数器，确保每次运行时都从0开始
    global printed_element_counter
    printed_element_counter = 0

    print(f"\n==== 应用程序启动: XML解析与过滤 ====")

    try:
        # 实例化我们的XML解析工具
        xml_tool_instance = XMLParserUtil(app_arguments.xml_source_path)

        # 启动解析过程，并传入回调函数以及目标标签
        xml_tool_instance.parse_and_handle_elements(
            target_node_name=app_arguments.filter_tag,
            element_callback=print_formatted_xml_node
        )
        print(f"\n==== 应用程序结束。成功显示了 {printed_element_counter} 个过滤后的XML节点。 ====\n")

    except FileNotFoundError as file_err:
        print(f"\n错误！文件操作失败: {file_err}")
    except Exception as general_err:
        print(f"\n程序运行期间发生意外故障: {general_err}")

if __name__ == "__main__":
    main()
import sys
import os
from lxml import etree
from functools import wraps
from collections import defaultdict

"""
采用装饰器模式和迭代解析方式,处理大型XML文件.
输出特定标签的树形结构和统计信息，支持命令行和 IDE 环境运行。
在有默认文件 P00734 时，无需在终端调用运行。
"""
class XMLHandler:
    def __init__(self, processor_func):
        self.processor = processor_func
        wraps(processor_func)(self)

    def __call__(self, xml_path, target_element):
        self._check_file(xml_path)

        ns = self._get_namespace(xml_path)
        qualified_tag = f"{{{ns}}}{target_element}" if ns else target_element

        count = 0
        context = etree.iterparse(xml_path, events=("end",), tag=qualified_tag)

        for _, elem in context:
            try:
                self.processor(elem)
            except Exception as e:
                print(f"处理元素时出错: {e}", file=sys.stderr)
            finally:
                elem.clear()
                count += 1
                # 清理已处理的父元素
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

        del context
        return count

    def _check_file(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件 {path} 不存在")
        if not path.lower().endswith('.xml'):
            raise ValueError("必须提供XML格式文件")

    def _get_namespace(self, path):
        try:
            for _, (_, uri) in etree.iterparse(path, events=("start-ns",)):
                return uri
            return ""
        except etree.XMLSyntaxError:
            return ""


class XMLAnalyzer:
    def __init__(self):
        self.tag_stats = defaultdict(int)

    def process_element(self, element, indent=0):
        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        self.tag_stats[tag] += 1

        spaces = "    " * indent
        print(f"{spaces}<{tag}>")

        if element.text and element.text.strip():
            print(f"{spaces}    Text: {element.text.strip()}")

        for child in element:
            self.process_element(child, indent + 1)

        print(f"{spaces}</{tag}>")

    def show_stats(self):
        print("\n元素统计:")
        for tag, cnt in sorted(self.tag_stats.items()):
            print(f"{tag}: {cnt}")


@XMLHandler
def analyze_xml_element(element):
    analyzer = XMLAnalyzer()
    analyzer.process_element(element)
    analyzer.show_stats()


if __name__ == "__main__":
    # 适配PyCharm运行的参数处理
    if len(sys.argv) < 3:
        # 如果没有参数，尝试使用默认值 这样方便在PyCharm中直接运行
        default_file = "P00734.xml"
        default_tag = "evidence"

        if os.path.exists(default_file):
            print(f"使用默认参数: 文件={default_file}, 标签={default_tag}")
            total = analyze_xml_element(default_file, default_tag)
            print(f"\n处理完成，共找到 {total} 个 '{default_tag}' 元素")
        else:
            print("请提供XML文件路径和目标元素标签")
            print("示例: python xml_analyzer.py P00734.xml entry")
            sys.exit(1)
    else:
        xml_file = sys.argv[1]
        elem_tag = sys.argv[2]
        try:
            total = analyze_xml_element(xml_file, elem_tag)
            print(f"\n处理完成，共找到 {total} 个 '{elem_tag}' 元素")
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

import sys
from lxml import etree
import os
from functools import wraps


def xml_tag_extractor(file_path=None):


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 配置文件路径
            xml_path = file_path or kwargs.get('xml_file_path', "P00734.xml")

            # 路径验证
            xml_path = os.path.abspath(xml_path)
            if not os.path.exists(xml_path):
                print(f"错误：文件不存在：{xml_path}", file=sys.stderr)
                return

            if not xml_path.lower().endswith('.xml'):
                print("错误：仅支持.xml格式文件", file=sys.stderr)
                return

            # 解析器内部类
            class XMLParser:
                def __init__(self):
                    self.namespace_map = {}
                    self.all_tags = set()

                def extract_tags(self):
                    try:
                        context = etree.iterparse(
                            xml_path,
                            events=('start',),
                            huge_tree=True,
                            remove_blank_text=True
                        )

                        for event, elem in context:
                            try:
                                self.all_tags.add(elem.tag)
                            finally:
                                self._safe_element_cleanup(elem)

                        self._parse_namespaces()
                        return self.all_tags

                    except Exception as e:
                        print(f"解析失败：{str(e)}", file=sys.stderr)
                        return set()
                    finally:
                        if 'context' in locals():
                            del context

                def _safe_element_cleanup(self, elem):
                    try:
                        parent = elem.getparent()
                        if parent is not None and len(parent) > 0:
                            while len(parent) > 3:
                                parent.remove(parent[0])
                    except Exception as e:
                        print(f"元素清理警告：{str(e)}", file=sys.stderr)

                def _parse_namespaces(self):
                    try:
                        context = etree.iterparse(
                            xml_path,
                            events=('start-ns',),
                            huge_tree=True
                        )

                        for event, ns in context:
                            prefix, uri = ns
                            self.namespace_map[prefix] = uri

                    except Exception as e:
                        print(f"命名空间解析警告：{str(e)}", file=sys.stderr)

                def format_tags(self, tags_set):
                    formatted = []
                    for tag in sorted(tags_set):
                        if '}' in tag:
                            ns_uri, local_name = tag[1:].split('}', 1)
                            prefix = [k for k, v in self.namespace_map.items() if v == ns_uri]
                            prefix = prefix[0] if prefix else ns_uri
                            formatted.append(f"{prefix}:{local_name}")
                        else:
                            formatted.append(tag)
                    return formatted

            # 执行解析
            parser = XMLParser()
            tags = parser.extract_tags()

            if tags:
                formatted_tags = parser.format_tags(tags)

                # 将解析结果传递给被装饰函数
                return func(formatted_tags, *args, **kwargs)
            else:
                return None

        return wrapper

    return decorator


# 使用示例
@xml_tag_extractor(file_path="P00734.xml")
def print_xml_tags(formatted_tags, *args, **kwargs):
    """打印XML标签的函数"""
    print(f"在文件中发现 {len(formatted_tags)} 个唯一标签：\n")
    for idx, tag in enumerate(formatted_tags, 1):
        print(f"{idx:03d}. {tag}")

    # 保存到文件
    with open("tags_list.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(formatted_tags))


if __name__ == "__main__":
    # 直接调用被装饰的函数
    print_xml_tags()
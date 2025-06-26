import sys
from lxml import etree
from os import path
from functools import wraps

class largeXMLDealer:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, fileName, elemTag):
        if not path.isfile(fileName):
            raise FileNotFoundError(f"文件 '{fileName}' 不存在。")
        if not fileName.endswith(".xml"):
            raise ValueError("输入文件必须是 .xml 格式。")

        count = 0
        ns = self._getNamespace(fileName)
        full_tag = f"{{{ns}}}{elemTag}" if ns else elemTag
        context = etree.iterparse(fileName, events=("end",), tag=full_tag)

        for event, elem in context:
            try:
                self.func(elem)
            except Exception as e:
                raise Exception(f"处理元素时出错: {e}")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):
        try:
            context = etree.iterparse(fileName, events=("start-ns",))
            for event, (prefix, uri) in context:
                return uri
            return ""
        except Exception:
            return ""

    def extract_structure(self, element):
        tag_counts = {}

        def _extract(elem, level=0):
            tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

            print("  " * level + f"<{tag}>")
            if elem.text and elem.text.strip():
                print("  " * (level + 1) + f"Text: {elem.text.strip()}")
            for child in elem:
                _extract(child, level + 1)
            print("  " * level + f"</{tag}>")

        _extract(element)
        print("\n标签统计：")
        for tag, count in tag_counts.items():
            print(f"{tag}: {count}")


@largeXMLDealer
def dealwithElement(elem):
    dealer = largeXMLDealer(lambda x: None)
    dealer.extract_structure(elem)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python script.py <XML文件> <标签名>")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]
    try:
        count = dealwithElement(fileName, elemTag)
        print(f"\n总共有 '{elemTag}' 标签的数量: {count}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
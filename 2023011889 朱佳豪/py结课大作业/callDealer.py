"""
本程序演示如何使用 XMLDecoratorParser 装饰器解析大型 XML 文件。
"""

from XMLDecoratorParser import XMLDecoratorParser

"""
修改 @XMLDecoratorParser("P00734.xml", "accession") 中的参数，
即可用于解析其他 XML 文件中的指定标签（例如 <accession>）。
"""

@XmlDecoratorParser("P00734.xml", "accession")
def handle_element(elem):
    """
    处理单个 XML 元素，示例中输出其文本内容。

    参数:
        elem (lxml.etree.Element): 当前处理的 XML 元素
    """
    if elem is not None:
        print(elem.text)


if __name__ == "__main__":
    total = handle_element()
    print(f"Total elements parsed: {total}")

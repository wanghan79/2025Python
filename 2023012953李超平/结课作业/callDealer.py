"""
本程序是调用 LargeXMLParser 解析大型 XML 文件的示例

作者：李超平
用途：Python 程序设计课结课作业
"""

from LargeXMLParser import LargeXMLParser

@LargeXMLParser("P00734.xml", "accession")
def dealwithElement(elem):
    """
    处理函数，这里直接输出给定标签的text

    参数:
        elem (lxml.etree.Element): 当前解析到的 XML 元素对象
    """
    if isinstance(elem, object):
        print(elem.text)


if __name__ == "__main__":
    print(f"Already parsed {dealwithElement()} XML elements!")

"""
修改 @LargeXMLParser("P00734.xml", "accession") 的参数即可解析指定文件的指定标签
"""



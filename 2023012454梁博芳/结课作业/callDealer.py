from largeXMLDealer import LargeXMLParser

@LargeXMLParser("P00734.xml", "score")
def dealwithElement(elem):
    """
    处理每个 <accession> 标签，并输出其文本内容

    参数:
        elem (lxml.etree.Element): 当前解析到的 XML 元素对象
    """
    text = elem.text.strip() if elem.text else ""
    print(f"Accession: {text}")

if __name__ == "__main__":
    # 执行解析并打印总数
    count = dealwithElement()

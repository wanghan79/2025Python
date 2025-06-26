def xml_parser_decorator(print_func):
    """
    XML大文件解析修饰器
    参数:
        print_func: 数据打印函数
    返回:
        装饰后的函数
    """
    import xml.etree.ElementTree as ET
    
    def wrapper(xml_file, element_tag):
        # 使用迭代解析处理大文件
        for event, elem in ET.iterparse(xml_file, events=('end',)):
            if elem.tag == element_tag:
                # 调用原始打印函数处理元素
                print_func(elem)
                # 清理已处理元素释放内存
                elem.clear()
    return wrapper

# 使用示例
if __name__ == "__main__":
    # 定义基础打印函数
    def print_element(element):
        print(f"元素: {element.tag}, 属性: {element.attrib}, 文本: {element.text}")
    
    # 应用装饰器
    xml_processor = xml_parser_decorator(print_element)
    
    print("XML解析示例:")
    # 实际使用示例 (需要真实XML文件)
    # xml_processor('large_data.xml', 'record')
    
    # 模拟示例
    from io import StringIO
    mock_xml = StringIO('''<root>
        <record id="1">Data1</record>
        <record id="2">Data2</record>
    </root>''')
    xml_processor(mock_xml, 'record')
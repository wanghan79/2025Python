from largeXMLDealer import xml_dealer

# XML文件路径
XML_FILE = "large_data.xml"

@xml_dealer(XML_FILE)
def print_element_data(element, prefix=">>>"):
    """
    打印XML元素数据的函数，被xml_dealer装饰
    
    参数:
        element (dict): XML元素字典，包含name、attributes和data
        prefix (str): 打印前缀
    """
    print(f"{prefix} 元素: {element['name']}")
    if element['attributes']:
        print(f"{prefix} 属性: {element['attributes']}")
    if element['data']:
        print(f"{prefix} 数据: {element['data']}")
    print(f"{prefix} {'-'*30}")

if __name__ == "__main__":
    print("开始处理XML文件...")
    print_element_data()
    print("XML文件处理完成。")
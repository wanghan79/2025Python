from xml_parser import XMLParserDecorator
import os


def create_sample_xml(file_path, num_items=1000):
    """创建示例XML文件（测试用）"""
    with open(file_path, 'w') as f:
        f.write('<?xml version="1.0"?>\n<catalog>\n')
        for i in range(num_items):
            f.write(f'<product id="p{i}">\n'
                    f'  <name>Product {i}</name>\n'
                    f'  <price>{19.99 + i}</price>\n'
                    f'</product>\n')
        f.write('</catalog>')


if __name__ == "__main__":
    # 1. 创建测试文件
    xml_file = "sample.xml"
    if not os.path.exists(xml_file):
        create_sample_xml(xml_file, 50)


    # 2. 基本使用示例
    @XMLParserDecorator.xml_parser(xml_file, "product")
    def print_product(data):
        print(f"{data['name']}: ${data['price']}")


    print("=== 基本示例 ===")
    print_product()


    # 3. 高级示例（带参数和返回值）
    @XMLParserDecorator.xml_parser(xml_file, "product")
    def filter_products(data, min_price=20):
        if float(data['price']) > min_price:
            return data


    print("\n=== 高价产品 ===")
    expensive = filter_products(min_price=25)
    for p in expensive:
        print(f"高价产品: {p['name']} (${p['price']})")
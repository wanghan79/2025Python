import csv
import xml.etree.ElementTree as ET

def file_parser_decorator(filepath, filetype='csv'):
    """
    文件解析装饰器，支持 CSV 和 XML
    :param filepath: 文件路径
    :param filetype: 'csv' 或 'xml'
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if filetype == 'csv':
                try:
                    with open(filepath, newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        data = list(reader)
                except FileNotFoundError:
                    print(f"文件 {filepath} 未找到")
                    return
            elif filetype == 'xml':
                try:
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    data = []
                    for child in root:
                        record = {elem.tag: elem.text for elem in child}
                        data.append(record)
                except FileNotFoundError:
                    print(f"文件 {filepath} 未找到")
                    return
            else:
                raise ValueError("Unsupported file type: use 'csv' or 'xml'")

            return func(data, *args, **kwargs)
        return wrapper
    return decorator
#使用范例
@file_parser_decorator('data.xml', filetype='xml')
def process_xml(data):
    print("XML数据如下：")
    for record in data:
        print(record)
    avg_score = sum(float(r['score']) for r in data) / len(data)
    print(f"平均分：{avg_score:.2f}")

process_xml()

@file_parser_decorator('data.csv', filetype='csv')
def process_csv(data):
    print("CSV数据如下：")
    for record in data:
        print(record)
    print(f"总人数：{len(data)}")

process_csv()
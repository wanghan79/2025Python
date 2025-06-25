import csv
import xml.etree.ElementTree as ET

def file_parser_decorator(filepath, filetype='csv'):
    """
    解析文件装饰器，支持 CSV 和 XML
    :param filepath: 文件路径
    :param filetype: 'csv' 或 'xml'
    """
    def decorator(func):
        # 执行解析
        if filetype == 'csv':
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        elif filetype == 'xml':
            tree = ET.parse(filepath)
            root = tree.getroot()
            data = []
            for child in root:
                record = {}
                for elem in child:
                    record[elem.tag] = elem.text
                data.append(record)
        else:
            raise ValueError("Unsupported file type: use 'csv' or 'xml'")

        # 内部包装器，把解析好的 data 传给业务函数
        def wrapper(*args, **kwargs):
            return func(data, *args, **kwargs)

        return wrapper
    return decorator
#范例csv
@file_parser_decorator('data.csv', filetype='csv')
def process_csv(data):
    print("CSV数据如下：")
    for record in data:
        print(record)
    print(f"总人数：{len(data)}")
process_csv()
#范例xml
@file_parser_decorator('data.xml', filetype='xml')
def process_xml(data):
    print("XML数据如下：")
    for record in data:
        print(record)
    avg_score = sum(float(r['score']) for r in data) / len(data)
    print(f"平均分：{avg_score:.2f}")
process_xml()

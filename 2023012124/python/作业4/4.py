import xml.etree.ElementTree as ET
from functools import wraps

def xml_parser_decorator(file_path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = []
            for elem in root.iter():
                data.append(elem.tag + ": " + (elem.text or '').strip())
            return func(data, *args, **kwargs)
        return wrapper
    return decorator

@xml_parser_decorator(file_path='large_file.xml')
def print_data(data):
    for line in data:
        print(line)

print_data()

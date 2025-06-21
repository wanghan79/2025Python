from lxml import etree
from os import path

def xml_parse_decorator(fileName, elemTag):
    """
    装饰器：解析大XML文件，将每个elemTag元素传递给被修饰函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not path.isfile(fileName) or not fileName.endswith("xml"):
                raise FileNotFoundError(f"{fileName} 不存在或不是xml文件")
            count = 0
            ns = _getNamespace(fileName)
            ns = "{%s}" % ns if ns else ""
            context = etree.iterparse(fileName, events=('end',), tag=ns + elemTag)
            for event, elem in context:
                func(elem, *args, **kwargs)
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
            del context
            print(f"Already parsed {count} XML elements.")
            return count
        return wrapper
    return decorator

def _getNamespace(fileName):
    if not path.isfile(fileName) or not fileName.endswith("xml"):
        raise FileNotFoundError
    result = ''
    context = etree.iterparse(fileName, events=('start-ns',))
    for event, elem in context:
        prefix, result = elem
        break
    del context
    return result
    import sys
from largeXMLDealer10 import xml_parse_decorator

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer11.py <xml_file> <element_tag>")
        sys.exit(1)
    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    @xml_parse_decorator(fileName, elemTag)
    def print_elem(elem):
        print(elem.text.strip() if elem.text else "")

    print_elem()  

import sys
from lxml import etree
from os import path

def xml_parser_decorator(elem_tag):
    def decorator(func):
        def wrapper(file_name):
            if not path.isfile(file_name) or not file_name.endswith("xml"):
                raise FileNotFoundError
            
            count = 0
            ns = ""
            try:
                context = etree.iterparse(file_name, events=('start-ns',))
                for event, elem in context:
                    ns = elem[1]
                    break
            except:
                ns = ""
            
            full_tag = f"{{{ns}}}{elem_tag}" if ns else elem_tag
            context = etree.iterparse(file_name, events=('end',), tag=full_tag)
            
            for event, elem in context:
                try:
                    func(elem)
                finally:
                    elem.clear()
                    count += 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            print(f"Already parsed {count} XML elements.")
        return wrapper
    return decorator

@xml_parser_decorator(elem_tag=sys.argv[2])
def print_element_text(elem):
    if isinstance(elem, object) and elem.text:
        print(elem.text.strip())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <xml_file> <element_tag>")
        sys.exit(1)
    print_element_text(sys.argv[1])

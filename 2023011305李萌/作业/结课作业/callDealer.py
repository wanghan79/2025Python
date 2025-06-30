import sys
from xml.etree import ElementTree

def process_xml(file_path, tag):
    def decorator(func):
        def wrapper():
            for event, elem in ElementTree.iterparse(file_path, events=('end',)):
                if elem.tag == tag:
                    func(elem)
                    elem.clear()
        return wrapper
    return decorator

if __name__ == "__main__":
    file_name, element_tag = sys.argv[1:3]
    
    @process_xml(file_name, element_tag)
    def handle_element(elem):
        if elem.text:
            print(elem.text.strip())
    
    handle_element()
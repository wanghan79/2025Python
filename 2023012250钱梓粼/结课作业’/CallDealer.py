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

import xml.sax
from functools import wraps
from typing import Callable, Dict, List


def xml_parser(file_path: str):
    def decorator(print_func: Callable):
        @wraps(print_func)
        def wrapper(*args, **kwargs):
            class XMLHandler(xml.sax.ContentHandler):
                def __init__(self):
                    self.current_data = ""
                    self.records = []
                    self.record = {}

                def startElement(self, tag, attrs):
                    self.current_data = tag
                    if tag == "record":
                        self.record = {}

                def characters(self, content):
                    if self.current_data and content.strip():
                        self.record[self.current_data] = content.strip()

                def endElement(self, tag):
                    if tag == "record":
                        self.records.append(self.record)
                    self.current_data = ""

            parser = xml.sax.make_parser()
            handler = XMLHandler()
            parser.setContentHandler(handler)
            parser.parse(file_path)

            return print_func(handler.records, *args, **kwargs)

        return wrapper

    return decorator


@xml_parser("large_data.xml")
def print_data(records: List[Dict], limit: int = 5):
    for i, record in enumerate(records[:limit], 1):
        print(f"Record {i}:")
        for key, value in record.items():
            print(f"  {key}: {value}")
        print()


if __name__ == "__main__":
    print_data(limit=3)
from functools import wraps
import xml.sax

def parse_xml(file_path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            class XMLHandler(xml.sax.ContentHandler):
                def __init__(self):
                    self.current_data = ""
                    self.content = ""
                    self.data_dict = {}

                def startElement(self, tag, attributes):
                    self.current_data = tag
                    self.content = ""

                def characters(self, content):
                    if self.current_data:
                        self.content += content.strip()

                def endElement(self, tag):
                    if self.current_data and self.content:
                        self.data_dict[self.current_data] = self.content
                    if tag == "root":
                        func(self.data_dict, *args, **kwargs)
                        self.data_dict = {}

            parser = xml.sax.make_parser()
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            handler = XMLHandler()
            parser.setContentHandler(handler)
            parser.parse(file_path)
        return wrapper
    return decorator

@parse_xml(r"C:\P00734.xml")
def callDealer(data):
    if data:
        print("解析结果：")
        for key, value in data.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    print("开始解析XML文件...")
    callDealer()
    print("解析完成")

import xml.sax
from functools import wraps


class LargeXMLDealer:
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = self.XMLHandler(func, *args, **kwargs)

            parser = xml.sax.make_parser()
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            parser.setContentHandler(handler)

            try:
                parser.parse(self.xml_file)
            except Exception as e:
                print(f"XML解析错误: {e}")
                raise

            return handler.results

        return wrapper

    class XMLHandler(xml.sax.ContentHandler):
        def __init__(self, func, *args, **kwargs):
            super().__init__()
            self.func = func
            self.args = args
            self.kwargs = kwargs
            self.current_data = {}
            self.results = []
            self.stack = []

        def startElement(self, tag, attrs):
            self.stack.append({
                'tag': tag,
                'attributes': dict(attrs),
                'content': []
            })

        def characters(self, content):
            if self.stack and content.strip():
                self.stack[-1]['content'].append(content.strip())

        def endElement(self, tag):
            if self.stack:
                element = self.stack.pop()
                node = {
                    'tag': element['tag'],
                    'attributes': element['attributes'],
                    'content': ''.join(element['content']),
                    'children': []
                }

                if self.stack:
                    self.stack[-1]['children'].append(node)
                else:
                    result = self.func(node, *self.args, **self.kwargs)
                    if result is not None:
                        self.results.append(result)
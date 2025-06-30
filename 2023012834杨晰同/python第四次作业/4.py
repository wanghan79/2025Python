import xml.sax
from functools import wraps
import os
import time
from collections import defaultdict
import sys


class XMLParserDecorator:
    """XML大文件解析装饰器核心类"""

    @staticmethod
    def xml_parser(xml_file, target_tag, max_items=None):
        def decorator(process_func):
            @wraps(process_func)
            def wrapper(*args, **kwargs):
                if not os.path.exists(xml_file):
                    raise FileNotFoundError(f"XML文件未找到: {xml_file}")

                print(f"开始解析 {xml_file} (目标标签: {target_tag})")
                start_time = time.time()

                parser = xml.sax.make_parser()
                parser.setFeature(xml.sax.handler.feature_namespaces, 0)
                handler = XMLParserDecorator.XMLHandler(
                    target_tag, process_func, *args, **kwargs
                )
                handler.max_items = max_items
                parser.setContentHandler(handler)

                try:
                    parser.parse(xml_file)
                except Exception as e:
                    print(f"解析错误: {str(e)}")
                    return

                duration = time.time() - start_time
                print(f"\n解析完成! 共处理 {handler.item_count} 项")
                print(f"耗时: {duration:.2f}秒 ({handler.item_count / duration:.2f} 项/秒)")
                return handler.processed_data

            return wrapper

        return decorator

    class XMLHandler(xml.sax.ContentHandler):
        """SAX处理器实现"""

        def __init__(self, target_tag, process_func, *args, **kwargs):
            self.target_tag = target_tag
            self.process_func = process_func
            self.process_args = args
            self.process_kwargs = kwargs
            self.current_data = {}
            self.in_target = False
            self.item_count = 0
            self.processed_data = []

import xml.sax
from functools import wraps
from typing import Callable, Any, List, Union, Dict, Optional


class XMLParser:
    """
    参数化类装饰器，用于解析中等规模XML文件

    参数:
        xml_file_path: XML文件路径
        target_tags: 需要处理的目标标签(单个字符串或字符串列表)
        encoding: 文件编码(默认'utf-8')
        verbose: 是否显示解析详情(默认False)
        attr_prefix: 属性名前缀(默认'@')
        text_key: 文本内容键名(默认'#text')
        max_elements: 最大处理元素数(默认None，表示无限制)
    """

    def __init__(self,
                 xml_file_path: str,
                 target_tags: Union[str, List[str]],
                 encoding: str = 'utf-8',
                 verbose: bool = False,
                 attr_prefix: str = '@',
                 text_key: str = '#text',
                 max_elements: Optional[int] = None):
        self.xml_file_path = xml_file_path
        self.target_tags = [target_tags] if isinstance(target_tags, str) else target_tags
        self.encoding = encoding
        self.verbose = verbose
        self.attr_prefix = attr_prefix
        self.text_key = text_key
        self.max_elements = max_elements
        self._element_count = 0

    def __call__(self, process_func: Callable[[Dict], Any]) -> Callable:
        """
        使实例可调用，作为装饰器使用

        参数:
            process_func: 处理每个解析出的数据元素的函数
        """

        @wraps(process_func)
        def wrapper(*args, **kwargs):
            if self.verbose:
                print(f"开始解析XML文件: {self.xml_file_path}")
                print(f"目标标签: {', '.join(self.target_tags)}")
                print(f"编码: {self.encoding}")
                if self.max_elements:
                    print(f"最大处理元素数: {self.max_elements}")

            class XMLContentHandler(xml.sax.ContentHandler):
                def __init__(self):
                    self.stack = []
                    self.current_element = None
                    self.current_content = ""
                    self.process_func = process_func
                    self.args = args
                    self.kwargs = kwargs
                    self.should_stop = False

                def startElement(self, tag: str, attrs: Dict):
                    if self.should_stop:
                        return

                    if tag in self.target_tags:
                        # 创建新元素并添加属性
                        self.current_element = {
                            '_tag': tag,
                            '_attrs': {f"{self.attr_prefix}{k}": v for k, v in attrs.items()},
                            '_children': {}
                        }
                        self.stack.append(self.current_element)
                    elif self.stack:
                        # 处理嵌套元素
                        self.current_content = ""
                        current = self.stack[-1]
                        if tag not in current['_children']:
                            current['_children'][tag] = []

                def characters(self, content: str):
                    if self.stack and not self.should_stop:
                        self.current_content += content.strip()

                def endElement(self, tag: str):
                    if self.should_stop or not self.stack:
                        return

                    current = self.stack[-1]

                    if tag == current['_tag']:
                        # 处理目标元素结束
                        element = {
                            **current['_attrs'],
                            **current['_children']
                        }

                        if self.current_content:
                            element[self.text_key] = self.current_content

                        self._element_count += 1

                        try:
                            self.process_func(element, *self.args, **self.kwargs)
                        except Exception as e:
                            if self.verbose:
                                print(f"处理元素时出错: {e}")

                        if self.max_elements and self._element_count >= self.max_elements:
                            self.should_stop = True

                        self.stack.pop()
                        self.current_content = ""
                    elif self.stack:
                        # 处理嵌套元素内容
                        parent = self.stack[-1]
                        if tag in parent['_children']:
                            if self.current_content:
                                parent['_children'][tag].append(self.current_content)
                            self.current_content = ""

                def endDocument(self):
                    if self.verbose:
                        print(f"解析完成，共处理 {self._element_count} 个目标元素")
                        if self.should_stop and self.max_elements:
                            print(f"已达到最大处理元素数 {self.max_elements}，提前终止解析")

            try:
                parser = xml.sax.make_parser()
                parser.setFeature(xml.sax.handler.feature_namespaces, 0)
                parser.setContentHandler(XMLContentHandler())
                parser.parse(self.xml_file_path)
            except xml.sax.SAXParseException as e:
                print(f"XML解析错误(行 {e.getLineNumber()}): {e.getMessage()}")
                raise
            except Exception as e:
                print(f"解析XML文件时出错: {e}")
                raise

        return wrapper
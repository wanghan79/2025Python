import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Callable, Any
from functools import wraps


class LargeXMLParser:
    def __init__(self, xml_file: str, namespaces: Optional[Dict[str, str]] = None):
        """
        初始化大型XML解析器

        参数:
            xml_file: XML文件路径
            namespaces: 命名空间映射字典
        """
        self.xml_file = xml_file
        self.namespaces = namespaces or {}

    def parse(self, element_path: str, chunk_size: int = 1000,
              callback: Optional[Callable[[Dict[str, Any]], Any]] = None) -> List[Dict[str, Any]]:
        """
        解析XML文件并返回元素数据

        参数:
            element_path: 要解析的元素路径
            chunk_size: 每次处理的元素数量
            callback: 处理每个元素的回调函数

        返回:
            包含解析数据的字典列表
        """
        results = []
        context = ET.iterparse(self.xml_file, events=('start', 'end'))

        # 转换为迭代器
        context = iter(context)

        # 获取根元素
        event, root = next(context)

        current_chunk = []
        for event, elem in context:
            if event == 'end' and self._match_element(elem, element_path):
                data = self._extract_element_data(elem)
                if callback:
                    data = callback(data)

                current_chunk.append(data)

                if len(current_chunk) >= chunk_size:
                    results.extend(current_chunk)
                    current_chunk = []
                    root.clear()  # 清除已处理的元素以节省内存

        # 添加剩余的块
        if current_chunk:
            results.extend(current_chunk)

        return results

    def _match_element(self, elem: ET.Element, path: str) -> bool:
        """检查元素是否匹配给定路径"""
        # 处理命名空间
        for prefix, uri in self.namespaces.items():
            ET.register_namespace(prefix, uri)

        # 简化路径匹配逻辑
        tag = elem.tag
        for uri in self.namespaces.values():
            tag = tag.replace(f'{{{uri}}}', '')

        return tag == path.split('}')[-1].split('/')[-1]

    def _extract_element_data(self, elem: ET.Element) -> Dict[str, Any]:
        """从元素中提取数据"""
        text = elem.text.strip() if elem.text and elem.text.strip() else None
        data = {
            'tag': elem.tag,
            'text': text,
            'attrib': elem.attrib,
            'children': [self._extract_element_data(child) for child in elem]
        }
        return data


def xml_parse_decorator(xml_file: str, element_path: str, **kwargs):
    """
    修饰器工厂函数，用于XML解析

    参数:
        xml_file: XML文件路径
        element_path: 要解析的元素路径
        **kwargs: 传递给LargeXMLParser的其他参数
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **inner_kwargs):
            parser = LargeXMLParser(xml_file, kwargs.get('namespaces'))
            data = parser.parse(element_path,
                                chunk_size=kwargs.get('chunk_size', 1000),
                                callback=kwargs.get('callback'))
            return func(data, *args, **inner_kwargs)

        return wrapper

    return decorator
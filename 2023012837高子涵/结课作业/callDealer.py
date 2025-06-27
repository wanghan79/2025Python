from typing import Dict, List, Any
from LargeXMLParse import LargeXMLParser, xml_parse_decorator
import pprint

# 定义命名空间（根据您的XML文件调整）
NAMESPACES = {
    'uniprot': 'http://uniprot.org/uniprot',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}


# 示例回调函数
def process_entry(entry_data: Dict[str, Any]) -> Dict[str, Any]:
    """处理每个entry元素的回调函数"""
    simplified = {
        'accession': [child['text'] for child in entry_data.get('children', [])
                      if child['tag'].endswith('accession')],
        'name': next((child['text'] for child in entry_data.get('children', [])
                      if child['tag'].endswith('name')), None),
        'protein': next((child for child in entry_data.get('children', [])
                         if child['tag'].endswith('protein')), None)
    }
    return simplified


# 使用修饰器方式处理XML
@xml_parse_decorator(
    'P00734.xml',
    '{http://uniprot.org/uniprot}entry',
    namespaces=NAMESPACES,
    chunk_size=50,
    callback=process_entry
)
def print_entries(entries: List[Dict[str, Any]], max_entries: int = 5):
    """打印条目数据"""
    pp = pprint.PrettyPrinter(indent=2)
    print(f"\nFound {len(entries)} entries. Showing first {max_entries}:")
    for i, entry in enumerate(entries[:max_entries]):
        print(f"\nEntry {i + 1}:")
        pp.pprint(entry)


# 直接使用解析器类
def parse_with_class():
    """直接使用LargeXMLParser类解析"""
    parser = LargeXMLParser('P00734.xml', NAMESPACES)
    entries = parser.parse(
        '{http://uniprot.org/uniprot}entry',
        chunk_size=50,
        callback=process_entry
    )

    print(f"\nTotal entries found: {len(entries)}")
    print("\nFirst entry details:")
    pprint.pprint(entries[0] if entries else {})


if __name__ == '__main__':
    print("=== Using decorator approach ===")
    print_entries(max_entries=3)

    print("\n=== Using class directly ===")
    parse_with_class()
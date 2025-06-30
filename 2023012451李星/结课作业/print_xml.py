from lxml import etree
from functools import wraps
from typing import Callable, List, Dict, Optional
import time


def xml_file_parser(
        xml_path: str,
        target_tag: str,
        chunk_size: int = 1000,
        encoding: str = 'utf-8'
):
    """
    XML大文件解析修饰器

    Args:
        xml_path (str): XML文件路径
        target_tag (str): 需要提取的目标标签名
        chunk_size (int): 每次处理的数据块大小（默认1000条）
        encoding (str): 文件编码（默认utf-8）

    Returns:
        Callable: 修饰后的数据处理函数
    """

    def decorator(process_func: Callable):
        @wraps(process_func)
        def wrapper(*args, **kwargs):
            print(f"Start parsing XML file: {xml_path}")
            start_time = time.time()

            # 使用lxml的迭代解析器
            context = etree.iterparse(
                xml_path,
                events=('end',),
                tag=target_tag,
                huge_tree=True
            )

            data_chunk = []
            for event, elem in context:
                # 提取当前元素数据
                data = {
                    child.tag: child.text for child in elem.iterchildren()
                    if child.text and child.text.strip()
                }
                if data:
                    data_chunk.append(data)

                # 达到chunk_size时处理数据
                if len(data_chunk) >= chunk_size:
                    process_func(data_chunk, *args, **kwargs)
                    data_chunk.clear()

                # 清理已处理元素，释放内存
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

            # 处理剩余数据
            if data_chunk:
                process_func(data_chunk, *args, **kwargs)

            # 计算耗时
            elapsed = time.time() - start_time
            print(f"Finished! Total time: {elapsed:.2f}s")

        return wrapper

    return decorator


def print_data(
        data: List[Dict],
        max_rows: int = 5,
        fields: Optional[List[str]] = None
) -> None:
    """
    打印数据（可被修饰的函数）

    Args:
        data (List[Dict]): 数据集
        max_rows (int): 最大打印行数（默认5）
        fields (List[str]): 指定打印的字段（默认全部）
    """
    if not data:
        print("No data to display.")
        return

    print("\n=== Data Preview ===")
    for i, item in enumerate(data[:max_rows]):
        display = {
            k: v for k, v in item.items()
            if not fields or k in fields
        }
        print(f"Row {i + 1}: {display}")
    if len(data) > max_rows:
        print(f"... and {len(data) - max_rows} more rows")


@xml_file_parser(
    xml_path="large_data.xml",
    target_tag="record",
    chunk_size=1000
)
def process_xml_data(data_chunk: List[Dict], fields: List[str]):
    """被修饰的数据处理函数"""
    print_data(data_chunk, fields=fields)


def generate_sample_xml(file_path: str, num_records: int = 10000):
    """生成示例XML文件（用于测试）"""
    root = etree.Element("data")
    for i in range(num_records):
        record = etree.SubElement(root, "record")
        etree.SubElement(record, "id").text = str(i)
        etree.SubElement(record, "name").text = f"Item_{i}"
        etree.SubElement(record, "value").text = str(round(i * 1.5, 2))

    with open(file_path, 'wb') as f:
        f.write(etree.tostring(root, encoding='utf-8', pretty_print=True))
    print(f"Generated sample XML: {file_path}")


def main():
    # 生成测试文件（10000条记录）
    generate_sample_xml("large_data.xml", num_records=10000)

    # 解析XML并打印数据（只显示id和name字段）
    process_xml_data(fields=["id", "name"])


if __name__ == "__main__":
    main()
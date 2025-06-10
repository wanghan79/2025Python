from lxml import etree

def print_tree(element, level=0):

    indent = "    " * level  # 每一层使用4个空格缩进
    print(f"{indent}{element.tag}")
    if element.text and element.text.strip():
        print(f"{indent}    Text: {element.text.strip()}")
    for child in element:
        print_tree(child, level + 1)

def main(xml_file):

    try:
        # 解析 XML 文件
        tree = etree.parse(xml_file)
        root = tree.getroot()

        # 打印根节点
        print(f"Root node: {root.tag}")
        print_tree(root)

    except FileNotFoundError:
        print(f"File not found: {xml_file}")
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python print_xml_tree.py <xml_file>")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    main(xml_file_path)
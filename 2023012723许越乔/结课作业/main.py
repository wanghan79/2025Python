import xml.etree.ElementTree as ET
from collections import defaultdict

class Node:
    def __init__(self, tag):
        self.tag = tag
        self.children = defaultdict(list)  # 记录子标签信息

    def add_child(self, child_node):
        self.children[child_node.tag].append(child_node)

    def get_depth(self):
        if not self.children:
            return 1
        return 1 + max(child.get_depth() for child in self.children.values())

def build_structure(element, depth, structure):
    tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag

    if tag_name not in structure[depth]:
        structure[depth].append(tag_name)

    max_depth = depth
    for child in element:
        if child.tag is not None:  # 忽略注释等特殊节点
            child_depth = build_structure(child, depth + 1, structure)
            if child_depth > max_depth:
                max_depth = child_depth
    return max_depth

def analyze_xml_structure(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        structure = defaultdict(list)

        # 构建结构信息
        max_depth = build_structure(root, 0, structure)

        # 转换为有序结构
        structure_dict = {k: sorted(v) for k, v in sorted(structure.items())}

        return structure_dict, max_depth

    except ET.ParseError as e:
        return None, f"XML解析错误: {str(e)}"
    except Exception as e:
        return None, str(e)

def build_tree(structure):
    if not structure:
        return "空结构"

    tree = {}

    for depth in sorted(structure.keys()):
        tags = structure[depth]
        if depth not in tree:
            tree[depth] = []
        for tag in tags:
            if tag not in tree[depth]:
                tree[depth].append(tag)

    tree_representation = ""
    for depth in sorted(tree.keys()):
        tree_representation += f"{depth}层: {', '.join(tree[depth])}\n"

    return tree_representation.strip()

def print_tree(structure):
    if not structure:
        print("空结构")
        return

    max_depth = max(structure.keys())

    root_tags = structure.get(0, [])
    for tag in root_tags:
        print(tag)

    for depth in range(1, max_depth + 1):
        tags = structure.get(depth, [])
        for tag in tags:
            indent = "  " * depth
            print(f"{indent}└── {tag}")

def main():
    file_path = input("请输入XML文件路径: ")

    structure, max_depth = analyze_xml_structure(file_path)
    if structure is None:
        print(f"分析失败: {max_depth}")
        return

    print("\nXML结构分析:")
    print(f"最大深度: {max_depth}层\n")

    print("树形结构:")
    print_tree(structure)

if __name__ == "__main__":
    main()
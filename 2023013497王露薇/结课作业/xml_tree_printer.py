import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict


def build_tag_tree(element, parent_path=""):
    """递归构建标签树结构"""
    current_path = f"{parent_path}/{element.tag}" if parent_path else element.tag
    children = {}

    # 处理当前元素的所有子元素
    for child in element:
        child_tag = child.tag
        if child_tag not in children:
            children[child_tag] = build_tag_tree(child, current_path)
        else:
            # 合并相同标签的子树
            existing_child = children[child_tag]
            new_child = build_tag_tree(child, current_path)
            children[child_tag] = merge_trees(existing_child, new_child)

    # 处理属性作为特殊的"标签"
    for attr in element.attrib:
        attr_tag = f"@{attr}"
        children[attr_tag] = {}

    return {element.tag: children}


def merge_trees(tree1, tree2):
    """合并两个树结构，保留所有唯一路径"""
    merged = defaultdict(dict)

    # 合并第一层标签
    for tag in set(tree1.keys()).union(tree2.keys()):
        if tag in tree1 and tag in tree2:
            merged[tag] = merge_trees(tree1[tag], tree2[tag])
        elif tag in tree1:
            merged[tag] = tree1[tag]
        else:
            merged[tag] = tree2[tag]

    return dict(merged)


def print_tree(tree, level=0, prefix=""):
    """格式化打印标签树"""
    for tag, children in tree.items():
        indent = "  " * level
        print(f"{indent}{prefix}{tag}")
        print_tree(children, level + 1)


def main():
    parser = argparse.ArgumentParser(description='生成XML文件的标签树结构')
    parser.add_argument('xml_file', help='XML文件路径')
    args = parser.parse_args()

    try:
        # 解析XML文件
        tree = ET.parse(args.xml_file)
        root = tree.getroot()

        # 构建标签树
        tag_tree = build_tag_tree(root)

        # 打印标签树
        print(f"XML文件 '{args.xml_file}' 的标签树结构：")
        print_tree(tag_tree)

    except FileNotFoundError:
        print(f"错误：找不到文件 '{args.xml_file}'")
    except ET.ParseError as e:
        print(f"XML解析错误：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")


if __name__ == "__main__":
    main()
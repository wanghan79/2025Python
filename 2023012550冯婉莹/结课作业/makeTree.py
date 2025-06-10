import xml.etree.ElementTree as ET
import sys  # 添加这一行导入sys模块
import os

def get_absolute_path(relative_path):
    return os.path.abspath(relative_path)

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False
    return True

def analyze_xml_structure(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 用于存储所有可能的路径
        all_paths = []

        def recurse(element, path):
            tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag
            current_path = path + [tag_name]

            if len(element) == 0:  # 如果是叶子节点
                all_paths.append(current_path)
            else:
                for child in element:
                    recurse(child, current_path)

        # 如果是森林，处理多个根节点
        if len(root) > 0 and root.tag is None:
            for child in root:
                recurse(child, [])
        else:
            recurse(root, [])

        return all_paths

    except ET.ParseError as e:
        print(f"XML解析失败: {e}")
        return []
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
        return []
    except Exception as e:
        print(f"未知错误: {e}")
        return []

def build_unique_tree(all_paths):
    if not all_paths:
        return "空结构"

    unique_tree = {}

    for path in all_paths:
        current_level = unique_tree
        for tag in path:
            if tag not in current_level:
                current_level[tag] = {}
            current_level = current_level[tag]

    return unique_tree

def print_tree(tree, indent=0):
    for key, value in tree.items():
        print(" " * indent + key)
        print_tree(value, indent + 4)

def main(file_path):
    absolute_path = get_absolute_path(file_path)
    print(f"绝对路径: {absolute_path}")

    if not check_file_exists(absolute_path):
        return

    all_paths = analyze_xml_structure(absolute_path)
    if not all_paths:
        print("XML结构分析: 空结构")
        return

    print("\nXML结构分析:")
    unique_tree = build_unique_tree(all_paths)
    if isinstance(unique_tree, str):
        print(unique_tree)
    else:
        print_tree(unique_tree)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python tx5.py <XML文件路径>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
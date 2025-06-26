import argparse
from lxml import etree

def print_xml_tree(element, level=0):
    """
    递归打印 XML 元素树
    :param element: 当前处理的 XML 元素
    :param level: 当前元素的层级
    """
    # 打印当前元素的标签和属性
    indent = "  " * level
    tag = element.tag
    # 移除命名空间前缀
    if '}' in tag:
        tag = tag.split('}')[1]
    attributes = " ".join([f"{k}='{v}'" for k, v in element.attrib.items()])
    if attributes:
        print(f"{indent}<{tag} {attributes}>")
    else:
        print(f"{indent}<{tag}>")

    # 打印元素的文本内容
    if element.text and element.text.strip():
        print(f"{indent}  {element.text.strip()}")

    # 递归处理子元素
    for child in element:
        print_xml_tree(child, level + 1)

    # 打印元素的结束标签
    print(f"{indent}</{tag}>")

def print_xml_file(file_path):
    """
    打印 XML 文件的数据树
    :param file_path: XML 文件的路径
    """
    try:
        # 解析 XML 文件
        parser = etree.XMLParser(recover=True, encoding='utf-8')
        with open(file_path, 'rb') as f:
            tree = etree.parse(f, parser)
        root = tree.getroot()

        # 处理森林情况，可能存在多个根元素
        if root.getparent() is None:
            if root.tag == etree.Comment:
                # 如果根是注释，跳过
                pass
            else:
                print_xml_tree(root)
            # 处理后续的兄弟元素
            for sibling in root.itersiblings():
                print_xml_tree(sibling)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
    except etree.XMLSyntaxError as e:
        print(f"XML 语法错误: {e}")
    except Exception as e:
        print(f"解析 XML 文件时出错: {e}")

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='打印 XML 文件的数据树')
    parser.add_argument('file_path', help='XML 文件的路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 使用命令行指定的文件路径
    print_xml_file(args.file_path)

    # 利用P00734.xml测试，输入如下命令 
    # python "C:\Users\15651\Desktop\Python课代码\案例分析3 large XML parser\案例分析3 large XML parser\xml_tree_printer.py" "C:\Users\15651\Desktop\Python课代码\案例分析3 large XML parser\案例分析3 large XML parser\P00734.xml"
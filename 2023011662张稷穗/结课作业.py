import sys
from os import path
from lxml import etree
from functools import wraps

def get_namespace(fileName):
    """获取XML文件的命名空间"""
    if not path.isfile(fileName) or not fileName.endswith(".xml"):
        raise FileNotFoundError(f"无效的 XML 文件: {fileName}")
    ns = ''
    for event, elem in etree.iterparse(fileName, events=('start-ns',)):
        _, ns = elem
        break
    return ns

def xml_parser(func):
    """修饰器，用于解析XML文件并处理指定标签的元素"""
    @wraps(func)
    def wrapper(fileName, elemTag):
        if not path.isfile(fileName) or not fileName.endswith(".xml"):
            raise FileNotFoundError(f"无效的 XML 文件: {fileName}")

        # 获取命名空间前缀
        ns_uri = get_namespace(fileName)
        ns_prefix = f"{{{ns_uri}}}" if ns_uri else ""
        count = 0

        # 解析XML文件
        context = etree.iterparse(fileName, events=('end',), tag=ns_prefix + elemTag)
        for event, elem in context:
            try:
                func(elem)  # 调用被修饰的函数处理元素
            except Exception as e:
                raise Exception(f"处理元素时出错: {e}")
            finally:
                elem.clear()  # 清理已处理的元素，释放内存
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    return wrapper

@xml_parser
def print_element(elem):
    """打印XML元素的文本内容"""
    print(elem.text)

def main():
    """主函数，解析命令行参数并调用解析器"""
    if len(sys.argv) != 3:
        print(f"用法: {sys.argv[0]} <XML 文件> <元素标签>")
        sys.exit(1)

    fileName, elemTag = sys.argv[1], sys.argv[2]
    count = print_element(fileName, elemTag)
    print(f"已经解析 {count} 个 XML 元素。")

if __name__ == "__main__":
    main()

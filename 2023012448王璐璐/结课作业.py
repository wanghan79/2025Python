from lxml import etree
from os import path
from functools import wraps

def xml_element_parser(func):
    """装饰器：解析指定标签的XML元素并逐个传递给处理函数"""
    @wraps(func)
    def wrapper(self, file_name, elem_tag, *args, **kwargs):
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError(f"Invalid XML file: {file_name}")
        
        ns = self._getNamespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        context = etree.iterparse(file_name, events=("end",), tag=ns_prefix + elem_tag)
        
        count = 0
        for event, elem in context:
            try:
                # 调用传入的处理函数
                func(self, elem, *args, **kwargs)
            except Exception as e:
                raise RuntimeError(f"Error processing element: {e}")
            finally:
                elem.clear()
                count += 1
                # 清理前兄弟节点释放内存
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        
        del context
        return count
    return wrapper

def xml_tree_parser(func):
    """装饰器：解析XML树状结构并传递给输出函数"""
    @wraps(func)
    def wrapper(self, file_name, root_tag=None, *args, **kwargs):
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError(f"Invalid XML file: {file_name}")
        
        ns = self._getNamespace(file_name)
        ns_prefix = f"{{{ns}}}" if ns else ""
        context = etree.iterparse(file_name, events=('start', 'end'))
        
        tree = {}
        path_stack = [tree]
        depth = 0

        for event, elem in context:
            if event == 'start':
                depth += 1
                current_tag = elem.tag.replace(ns_prefix, '')
                
                if depth == 1 and root_tag and current_tag != root_tag:
                    continue
                
                new_node = {}
                path_stack[-1][current_tag] = new_node
                path_stack.append(new_node)
                
            elif event == 'end':
                depth -= 1
                if depth > 0:
                    path_stack.pop()
                
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        
        del context
        # 调用输出函数并返回结果
        return func(self, tree, *args, **kwargs)
    return wrapper

class LargeXMLDealer:
    def _getNamespace(self, file_name):
        """获取XML命名空间"""
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError
        context = etree.iterparse(file_name, events=('start-ns',))
        for event, elem in context:
            return elem[1]  # 返回命名空间URI
        return ''

    @xml_element_parser
    def process_accession(self, elem):
        """处理accession元素"""
        print(elem.text)

    @xml_element_parser
    def process_sequence(self, elem):
        """处理sequence元素"""
        print(elem.text)

    @xml_tree_parser
    def output_tree(self, tree_data, indent=0, is_last=True, prefix=""):
        """输出XML树状结构（带修饰器版本）"""
        if not tree_data:
            return
        
        for i, (tag, children) in enumerate(tree_data.items()):
            is_last_child = i == len(tree_data) - 1
            
            # 打印当前节点
            if indent == 0:
                print(tag)
            else:
                symbol = "└── " if is_last_child else "├── "
                print(f"{prefix}{symbol}{tag}")
            
            # 递归打印子节点
            new_prefix = prefix + ("    " if is_last else "│   ")
            self.output_tree(children, indent+1, is_last_child, new_prefix)

# 使用示例
if __name__ == "__main__":
    dealer = LargeXMLDealer()
    
    # 处理accession元素
    accession_count = dealer.process_accession("P00734.xml", "accession")
    print(f"Processed {accession_count} accession elements")
    
    # 处理sequence元素
    sequence_count = dealer.process_sequence("P00734.xml", "sequence")
    print(f"Processed {sequence_count} sequence elements")
    
    # 输出树状结构
    dealer.output_tree("P00734.xml")

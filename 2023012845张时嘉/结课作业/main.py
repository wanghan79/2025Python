from lxml import etree
from functools import wraps

def xml_parser_decorator(file_path, target_tag):
    """XML 大文件解析修饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
         
            context = etree.iterparse(
                file_path,
                tag=target_tag,  
                events=('end',),  
                huge_tree=True  
            )
            data_list = []
            for event, elem in context:
                data = elem.text.strip() if elem.text else ""
                data_list.append(data)
                elem.clear()  
      
            return func(data_list, *args, **kwargs)
        return wrapper
    return decorator

@xml_parser_decorator(file_path="large_file.xml", target_tag="item")
def print_data(data_list):
    """打印解析后的 XML 数据"""
    print("解析到的数据条目数:", len(data_list))
    for idx, data in enumerate(data_list[:5], 1): 
        print(f"第 {idx} 条数据:", data)
    if len(data_list) > 5:
        print(f"... 共 {len(data_list)} 条数据（仅展示前5条）")

if __name__ == "__main__":
    print_data()

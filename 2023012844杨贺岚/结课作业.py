import xml.etree.ElementTree as ET
import os
import sys
import gzip
from functools import wraps
from typing import Callable, Generator, Dict, Any

def xml_parser_decorator(
    file_path: str, 
    element_name: str, 
    encoding: str = 'utf-8',
    gzipped: bool = False
) -> Callable:

    def decorator(process_func: Callable) -> Callable:

        @wraps(process_func)
        def wrapper(*args, **kwargs) -> Generator[Dict[str, Any], None, None]:

            try:
                if gzipped:
                    with gzip.open(file_path, 'rb') as f:
                        file_size = os.path.getsize(file_path)
                        print(f"开始解析GZIP压缩的XML文件: {file_path} (大小: {file_size/1024/1024:.2f} MB)")
                        yield from parse_large_xml(f, element_name, process_func, encoding)
                else:
                    file_size = os.path.getsize(file_path)
                    print(f"开始解析XML文件: {file_path} (大小: {file_size/1024/1024:.2f} MB)")
                    with open(file_path, 'r', encoding=encoding) as f:
                        yield from parse_large_xml(f, element_name, process_func, encoding)
            
            except FileNotFoundError:
                print(f"错误: 文件未找到 - {file_path}", file=sys.stderr)
            except ET.ParseError as e:
                print(f"XML解析错误: {e}", file=sys.stderr)
            except Exception as e:
                print(f"未知错误: {e}", file=sys.stderr)
        
        return wrapper
    return decorator

def parse_large_xml(
    file_obj, 
    element_name: str, 
    process_func: Callable, 
    encoding: str
) -> Generator[Dict[str, Any], None, None]:

    context = ET.iterparse(file_obj, events=('start', 'end'))
    
    _, root = next(context)
    
    element_count = 0
    print(f"查找元素: {element_name}")
    
    for event, elem in context:
        if event == 'end' and elem.tag == element_name:
            element_count += 1
            
            if element_count % 1000 == 0:
                sys.stdout.write(f"\r已解析元素: {element_count}")
                sys.stdout.flush()
            
            element_data = {
                'tag': elem.tag,
                'attrib': elem.attrib,
                'text': elem.text.strip() if elem.text else None,
                'children': {}
            }
            
            for child in elem:
                child_data = {
                    'tag': child.tag,
                    'attrib': child.attrib,
                    'text': child.text.strip() if child.text else None
                }
                # 处理多个同名的子元素
                if child.tag in element_data['children']:
                    if isinstance(element_data['children'][child.tag], list):
                        element_data['children'][child.tag].append(child_data)
                    else:
                        element_data['children'][child.tag] = [element_data['children'][child.tag], child_data]
                else:
                    element_data['children'][child.tag] = child_data
            
            processed_data = process_func(element_data)
            
            elem.clear()
            root.clear()
            
            if processed_data is not None:
                yield processed_data
    
    print(f"\n解析完成! 共找到 {element_count} 个 {element_name} 元素")

# 使用示例
if __name__ == "__main__":
    # 解析大型XML文件并打印基本信息
    @xml_parser_decorator('large_data.xml', 'product')
    def print_product_info(product_data: Dict) -> Dict:
        """
        打印产品基本信息
        """
        return {
            'id': product_data['attrib'].get('id'),
            'name': product_data['attrib'].get('name'),
            'category': product_data['children'].get('category', {}).get('text'),
            'price': product_data['children'].get('price', {}).get('text')
        }
    
    print("\n示例1: 打印产品基本信息")
    for i, product in enumerate(print_product_info()):
        if i < 5:  # 只打印前5个产品
            print(f"产品 {i+1}: {product}")
        if i >= 100:  # 只处理前100个产品用于演示
            break
    
    #解析GZIP压缩的XML文件并计算统计信息
    @xml_parser_decorator('large_data.xml.gz', 'transaction', gzipped=True)
    def calculate_transaction_stats(transaction_data: Dict) -> Dict:
        amount = float(transaction_data['children'].get('amount', {}).get('text', 0))
        
        return {
            'transaction_id': transaction_data['attrib'].get('id'),
            'amount': amount,
            'is_high_value': amount > 1000
        }

    print("\n示例2: 计算交易统计信息")
    total_amount = 0
    high_value_count = 0
    transaction_count = 0
    
    for i, transaction in enumerate(calculate_transaction_stats()):
        total_amount += transaction['amount']
        if transaction['is_high_value']:
            high_value_count += 1
        transaction_count += 1
        if i >= 100: 
            break
    
    print(f"交易总数: {transaction_count}")
    print(f"总交易金额: {total_amount:.2f}")
    print(f"高价值交易数量: {high_value_count}")
    print(f"高价值交易占比: {high_value_count/transaction_count*100:.1f}%")
    
    #自定义数据处理函数
    @xml_parser_decorator('users.xml', 'user')
    def process_user_data(user_data: Dict) -> Dict:
    
        user_id = user_data['attrib'].get('id')
        username = user_data['children'].get('username', {}).get('text')
        email = user_data['children'].get('email', {}).get('text')
        age = int(user_data['children'].get('age', {}).get('text', 0))
        
        address = user_data['children'].get('address', {})
        city = address.get('children', {}).get('city', {}).get('text')
        country = address.get('children', {}).get('country', {}).get('text')
        
        tags = []
        tags_elem = user_data['children'].get('tags', {})
        if isinstance(tags_elem, list):
            for tag in tags_elem:
                tags.append(tag['text'])
        elif tags_elem:
            tags.append(tags_elem['text'])
        
        return {
            'user_id': user_id,
            'username': username,
            'email': email,
            'age': age,
            'age_group': 'child' if age < 18 else 'adult' if age < 65 else 'senior',
            'location': f"{city}, {country}" if city and country else None,
            'tags': tags
        }
    
    print("\n示例3: 处理用户数据")
    for i, user in enumerate(process_user_data()):
        if i < 3: 
            print(f"用户 {i+1}:")
            print(f"  ID: {user['user_id']}")
            print(f"  用户名: {user['username']}")
            print(f"  邮箱: {user['email']}")
            print(f"  年龄: {user['age']} ({user['age_group']})")
            print(f"  位置: {user['location']}")
            print(f"  标签: {', '.join(user['tags'])}")
        if i >= 5:  # 只处理前5个用户用于演示
            break

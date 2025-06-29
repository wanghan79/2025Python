from largeXMLDealer import LargeXMLDealer


# 示例修饰器应用
@LargeXMLDealer("data/large_data.xml")
def process_book(book_node, min_price=0):
    """处理书籍数据的示例函数"""
    if book_node['tag'] == 'book':
        try:
            price = float(book_node['attributes'].get('price', '0'))
            if price >= min_price:
                return {
                    'title': book_node['attributes'].get('title'),
                    'author': next(
                        (c['content'] for c in book_node['children']
                         if c['tag'] == 'author'), ''),
                    'price': price
                }
        except ValueError:
            pass
    return None


# 示例修饰器应用 - 简单打印
@LargeXMLDealer("data/large_data.xml")
def simple_printer(node, tags_to_print=None):
    """简单打印XML节点的函数"""
    if tags_to_print is None or node['tag'] in tags_to_print:
        print(f"节点: {node['tag']}")
        if node['attributes']:
            print("属性:")
            for k, v in node['attributes'].items():
                print(f"  {k}: {v}")
        if node['content']:
            print(f"内容: {node['content']}")
        print("-" * 40)


if __name__ == "__main__":
    # 示例1: 处理高价书籍
    print("高价书籍:")
    expensive_books = process_book(min_price=50)
    for book in expensive_books[:5]:  # 只显示前5本
        print(book)

    # 示例2: 简单打印特定标签
    print("\n打印特定标签:")
    simple_printer(tags_to_print={'title', 'author'})
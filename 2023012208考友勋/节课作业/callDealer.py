# callDealer.py
from largeXMLDealer import large_xml_dealer, extract_entry_data
import pprint

@large_xml_dealer("P00734.xml")
def print_uniprot_data(entry_data, pretty_print=True):
    """
    被修饰的数据打印函数，用于展示UNIPROT条目信息
    
    Args:
        entry_data: 解析出的条目数据
        pretty_print: 是否美化打印
        
    Returns:
        无返回值，直接打印数据
    """
    print("\n" + "="*50)
    print(f"UNIPROT 条目解析: {entry_data['accessions'][0]}")
    print("="*50)
    
    print(f"主 Accession: {entry_data['accessions'][0]}")
    print(f"其他 Accession: {', '.join(entry_data['accessions'][1:])}")
    print(f"蛋白质名称: {entry_data['protein_name']}")
    print(f"基因名称: {entry_data['gene']}")
    print(f"物种: {entry_data['organism']}")
    
    print("\n参考文献:")
    for i, ref in enumerate(entry_data['references'], 1):
        print(f"  文献 {i}: {ref['title']}")
        if ref['authors']:
            print(f"    作者: {', '.join(ref['authors'][:3])}{'...' if len(ref['authors']) > 3 else ''}")
    
    print("="*50 + "\n")
    
    # 如需返回数据进行后续处理，可在此添加返回逻辑
    return None

def print_condensed_data(entry_data):
    """简洁版数据打印函数，用于演示修饰器的灵活性"""
    print(f"[简洁模式] Accession: {entry_data['accessions'][0]}, 蛋白质: {entry_data['protein_name']}")

def main():
    print("=== 完整数据打印模式 ===")
    # 调用修饰后的函数，数据会直接打印到控制台
    print_uniprot_data()
    
    # 演示修饰器的灵活性：可以将输出重定向到文件
    print("\n=== 重定向输出到文件 ===")
    from largeXMLDealer import redirect_stdout
    
    with redirect_stdout("uniprot_output.txt"):
        print_uniprot_data()
    
    print("数据已保存到 uniprot_output.txt")
    
    # 演示如何使用修饰器处理不同的打印函数
    print("\n=== 简洁数据打印模式 ===")
    # 创建一个临时修饰器用于简洁模式
    condensed_decorator = large_xml_dealer("P00734.xml")
    decorated_condensed_func = condensed_decorator(print_condensed_data)
    decorated_condensed_func()

if __name__ == "__main__":
    main()

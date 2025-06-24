# largeXMLDealer.py
import xml.etree.ElementTree as ET
from functools import wraps
import time
import sys
from contextlib import contextmanager

NAMESPACE = "{http://uniprot.org/uniprot}"
ENTRY_TAG = f"{NAMESPACE}entry"
PROTEIN_TAG = f"{NAMESPACE}protein"
RECOMMENDED_NAME_TAG = f"{NAMESPACE}recommendedName"
FULL_NAME_TAG = f"{NAMESPACE}fullName"
ACCESSION_TAG = f"{NAMESPACE}accession"
GENE_TAG = f"{NAMESPACE}gene"
ORGANISM_TAG = f"{NAMESPACE}organism"
SCIENTIFIC_NAME_TAG = f"{NAMESPACE}name[@type='scientific']"
REFERENCE_TAG = f"{NAMESPACE}reference"
CITATION_TAG = f"{NAMESPACE}citation"
TITLE_TAG = f"{NAMESPACE}title"
AUTHOR_LIST_TAG = f"{NAMESPACE}authorList"
PERSON_TAG = f"{NAMESPACE}person"

def large_xml_dealer(file_path):
    """
    修饰器工厂函数，用于处理大XML文件的流式解析
    
    Args:
        file_path: XML文件路径
        
    Returns:
        修饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 记录开始时间
            start_time = time.time()
            print(f"开始解析XML文件: {file_path}")
            
            # 初始化解析器和命名空间
            context = ET.iterparse(file_path, events=('start', 'end'))
            context = iter(context)
            event, root = next(context)
            
            entry_count = 0
            processed_data = []
            
            # 流式解析处理
            for event, elem in context:
                if event == 'end' and elem.tag == ENTRY_TAG:
                    # 提取条目数据
                    entry_data = extract_entry_data(elem)
                    processed_data.append(entry_data)
                    
                    # 调用被修饰函数处理数据
                    func_output = func(entry_data, *args, **kwargs)
                    if func_output is not None:
                        processed_data.extend(func_output)
                    
                    # 重置元素以释放内存
                    root.clear()
                    entry_count += 1
                    
                    # 定期输出进度
                    if entry_count % 10 == 0:
                        print(f"已处理 {entry_count} 个条目...")
            
            # 解析完成统计
            end_time = time.time()
            print(f"解析完成，共处理 {entry_count} 个条目")
            print(f"解析耗时: {end_time - start_time:.2f} 秒")
            
            return processed_data
        return wrapper
    return decorator

def extract_entry_data(entry_elem):
    """提取UNIPROT条目中的关键数据"""
    data = {
        "accessions": [],
        "protein_name": "",
        "gene": "",
        "organism": "",
        "references": []
    }
    
    # 提取 accession 号
    for accession_elem in entry_elem.findall(ACCESSION_TAG):
        data["accessions"].append(accession_elem.text)
    
    # 提取蛋白质名称
    protein_elem = entry_elem.find(PROTEIN_TAG)
    if protein_elem:
        recommended_name = protein_elem.find(RECOMMENDED_NAME_TAG)
        if recommended_name:
            full_name = recommended_name.find(FULL_NAME_TAG)
            if full_name:
                data["protein_name"] = full_name.text
    
    # 提取基因名称
    gene_elem = entry_elem.find(GENE_TAG)
    if gene_elem:
        gene_name = gene_elem.find(f"{NAMESPACE}name[@type='primary']")
        if gene_name:
            data["gene"] = gene_name.text
    
    # 提取物种信息
    organism_elem = entry_elem.find(ORGANISM_TAG)
    if organism_elem:
        scientific_name = organism_elem.find(SCIENTIFIC_NAME_TAG)
        if scientific_name:
            data["organism"] = scientific_name.text
    
    # 提取参考文献
    for ref_elem in entry_elem.findall(REFERENCE_TAG):
        citation_elem = ref_elem.find(CITATION_TAG)
        if citation_elem:
            title_elem = citation_elem.find(TITLE_TAG)
            title = title_elem.text if title_elem else "无标题"
            
            authors = []
            author_list = citation_elem.find(AUTHOR_LIST_TAG)
            if author_list:
                for person in author_list.findall(PERSON_TAG):
                    name = person.get("name")
                    if name:
                        authors.append(name)
            
            ref_data = {
                "title": title,
                "authors": authors
            }
            data["references"].append(ref_data)
    
    return data

@contextmanager
def redirect_stdout(file_path=None):
    """重定向标准输出到文件或保持原样"""
    original_stdout = sys.stdout
    if file_path:
        with open(file_path, 'w') as f:
            sys.stdout = f
            yield
            sys.stdout = original_stdout
    else:
        yield original_stdout

import xml.etree.ElementTree as ET
from functools import wraps

def xml_parser_decorator(func):
    """
    用于解析 XML文件的装饰器
    处理XML解析并将提取的数据传递给目标函数
    """
    @wraps(func)
    def wrapper(file_path, *args, **kwargs):
        # 定义命名空间
        ns = {'uniprot': 'http://uniprot.org/uniprot'}
        
        # 使用iterparse进行迭代解析，避免内存问题
        extracted_data = []
        for event, elem in ET.iterparse(file_path, events=('end',)):
            if elem.tag == f'{{{ns["uniprot"]}}}entry':
                data = {}
                
                # 提取accession列表
                data['accessions'] = [acc.text for acc in elem.findall('uniprot:accession', ns)]
                
                # 提取蛋白质名称
                name_elem = elem.find('uniprot:name', ns)
                data['name'] = name_elem.text if name_elem is not None else "N/A"
                
                # 提取蛋白质描述
                protein = {}
                protein_elem = elem.find('uniprot:protein', ns)
                if protein_elem:
                    rec_name = protein_elem.find('uniprot:recommendedName/uniprot:fullName', ns)
                    protein['recommendedName'] = rec_name.text if rec_name else "N/A"
                    
                    alt_names = [alt.text for alt in protein_elem.findall('uniprot:alternativeName/uniprot:fullName', ns)]
                    protein['alternativeNames'] = alt_names
                
                data['protein'] = protein
                
                # 提取基因信息
                gene_elem = elem.find('uniprot:gene/uniprot:name[@type="primary"]', ns)
                data['gene'] = gene_elem.text if gene_elem else "N/A"
                
                # 提取生物体信息
                organism = {}
                org_elem = elem.find('uniprot:organism', ns)
                if org_elem:
                    organism['scientific'] = org_elem.find('uniprot:name[@type="scientific"]', ns).text
                    organism['common'] = org_elem.find('uniprot:name[@type="common"]', ns).text
                    organism['taxonomy'] = org_elem.find('uniprot:dbReference[@type="NCBI Taxonomy"]', ns).attrib.get('id', 'N/A')
                
                data['organism'] = organism
                
                # 提取参考文献
                references = []
                for ref in elem.findall('uniprot:reference', ns):
                    ref_data = {}
                    citation = ref.find('uniprot:citation', ns)
                    if citation:
                        ref_data['type'] = citation.get('type', 'N/A')
                        ref_data['title'] = citation.find('uniprot:title', ns).text if citation.find('uniprot:title', ns) is not None else "N/A"
                        
                        # 处理作者列表
                        authors = []
                        author_list = citation.find('uniprot:authorList', ns)
                        if author_list:
                            authors = [author.get('name') for author in author_list.findall('uniprot:person', ns)]
                        ref_data['authors'] = authors
                    
                    references.append(ref_data)
                
                data['references'] = references
                extracted_data.append(data)
                
                # 清理元素以节省内存
                elem.clear()
        
        # 将解析后的数据传递给目标函数
        return func(extracted_data, *args, **kwargs)
    
    return wrapper
if __name__ == "__main__":
    xml_file = "P00734.xml"  
    print_protein_data(xml_file)

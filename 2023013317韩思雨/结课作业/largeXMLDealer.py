#!/usr/bin/env python
# coding:utf-8

from lxml import etree
from os import path
import argparse

UNIPROT_NS = "http://uniprot.org/uniprot"


class UniProtXMLParser:
    """专门处理UniProt XML格式的解析器"""

    def __init__(self):
        self.nsmap = {'up': UNIPROT_NS}

    def parse_components(self, xml_file):
        """解析组件信息"""
        if not path.isfile(xml_file):
            raise FileNotFoundError(f"文件未找到: {xml_file}")

        components = []
        for event, elem in etree.iterparse(xml_file, tag=f"{{{UNIPROT_NS}}}component"):
            component = self._parse_component(elem)
            if component:
                components.append(component)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        return components

    def _parse_component(self, component_elem):
        """解析单个component元素"""
        result = {
            'recommended_name': None,
            'alternative_names': []
        }

        # 解析推荐名称
        rec_name = component_elem.find("up:recommendedName/up:fullName", namespaces=self.nsmap)
        if rec_name is not None and rec_name.text:
            result['recommended_name'] = rec_name.text.strip()

        # 解析备用名称
        alt_names = component_elem.findall("up:alternativeName/up:fullName", namespaces=self.nsmap)
        result['alternative_names'] = [name.text.strip() for name in alt_names if name.text]

        return result if result['recommended_name'] or result['alternative_names'] else None

    def parse_accessions(self, xml_file):
        """解析accession号码"""
        accessions = []
        for event, elem in etree.iterparse(xml_file, tag=f"{{{UNIPROT_NS}}}accession"):
            if elem.text:
                accessions.append(elem.text.strip())
            elem.clear()
        return accessions


def print_component_info(component):
    """打印组件信息"""
    if component['recommended_name']:
        print(f"■ 主要名称: {component['recommended_name']}")
    for i, name in enumerate(component['alternative_names'], 1):
        print(f"  ▸ 备用名称{i}: {name}")
    print("-" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UniProt XML解析器")
    parser.add_argument("file", help="UniProt XML文件路径")
    parser.add_argument("--components", action="store_true", help="解析组件信息")
    parser.add_argument("--accessions", action="store_true", help="解析accession号码")

    args = parser.parse_args()

    parser = UniProtXMLParser()

    if args.components:
        print("[开始解析组件信息]")
        components = parser.parse_components(args.file)
        for comp in components:
            print_component_info(comp)
        print(f"共找到 {len(components)} 个组件")

    if args.accessions:
        print("\n[开始解析accession号码]")
        accessions = parser.parse_accessions(args.file)
        for acc in accessions:
            print(f"Accession: {acc}")
        print(f"共找到 {len(accessions)} 个accession号码")
"""
终端运行示例
python largeXMLDealer.py P00
734.xml --components
[开始解析组件信息]
■ 主要名称: Activation peptide fragment 1
----------------------------------------
■ 主要名称: Activation peptide fragment 2
----------------------------------------
■ 主要名称: Thrombin light chain
----------------------------------------
■ 主要名称: Thrombin heavy chain
----------------------------------------
共找到 4 个组件
python largeXMLDealer.py P00
734.xml --accessions

[开始解析accession号码]
Accession: P00734
Accession: B2R7F7
Accession: B4E1A7
Accession: Q4QZ40
Accession: Q53H04
Accession: Q53H06
Accession: Q69EZ7
Accession: Q7Z7P3
Accession: Q9UCA1
共找到 9 个accession号码
"""

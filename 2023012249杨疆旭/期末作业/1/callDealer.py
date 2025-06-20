
#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys

def dealwithElement(elem):
    ns = "{http://uniprot.org/uniprot}"
    print("=" * 60)
    print("【条目名称】:", elem.findtext(f"{ns}name"))

    print("【Accession 列表】:")
    for acc in elem.findall(f"{ns}accession"):
        print(" -", acc.text)

    full_name = elem.findtext(f".//{ns}recommendedName/{ns}fullName")
    print("【蛋白推荐名】:", full_name)

    print("【蛋白别名】:")
    for alt in elem.findall(f".//{ns}alternativeName/{ns}fullName"):
        print(" -", alt.text)

    print("【基因名称】:", elem.findtext(f".//{ns}gene/{ns}name"))
    print("【来源物种】:", elem.findtext(f".//{ns}organism/{ns}name[@type='scientific']"))

    seq = elem.findtext(f"{ns}sequence")
    print("【蛋白序列】:")
    if seq:
        print(seq.strip())

    print("【相关文献标题】:")
    for ref in elem.findall(f"{ns}reference/{ns}citation/{ns}title"):
        print(" -", ref.text)

    print("【PDB 数据库 ID】:")
    for db in elem.findall(f"{ns}dbReference[@type='PDB']"):
        print(" -", db.attrib.get("id"))
    print("=" * 60 + "\n")

if __name__ == "__main__":
    fileName = "P00734.xml"
    elemTag = "entry"

    lxmld = largeXMLDealer.largeXMLDealer()
    count = lxmld.parse(fileName, elemTag, dealwithElement)

import xml.etree.ElementTree as ET

def myparser(func):
    def inner():
        tree = ET.parse("P00734.xml")
        root = tree.getroot()
        ns = {"u": "http://uniprot.org/uniprot"}
        acc = []
        for a in root.findall("u:entry/u:accession", ns):
            acc.append(a.text)
        return func(acc)
    return inner

@myparser
def output(x):
    for i in x:
        print(i)

output()

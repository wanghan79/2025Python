#!/usr/bin/env python
# coding:utf-8

from largeXMLDealer import parse_xml_elements
import sys


def default_handler(elem):
    """
    默认处理函数：打印元素文本内容
    """
    if elem.text and elem.text.strip():
        print(elem.text.strip())


def main():
    if len(sys.argv) < 3:
        print("Usage: python callDealer.py <filename.xml> <tag_name>")
        print("Example: python callDealer.py P00734.xml accession")
        sys.exit(1)

    xml_file = sys.argv[1]
    tag_name = sys.argv[2]

    @parse_xml_elements(xml_file, tag_name)
    def handler(elem):
        default_handler(elem)

    # 触发解析过程
    handler()


if __name__ == "__main__":
    main()


'''
CALL EXAMPLE 1:
COMMAND LINE:     python callDealer.py P00734.xml accession
OUTPUT:           
P00734
B2R7F7
B4E1A7
Q4QZ40
Q53H04
Q53H06
Q69EZ7
Q7Z7P3
Q9UCA1
Already parsed 9 XML elements.          


CALL EXAMPLE 2:
COMMAND LINE:     python callDealer.py P00734.xml sequence
OUTPUT:           
MAHVRGLQLPGCLALAALCSLVHSQHVFLAPQQARSLLQRVRRANTFLEEVRKGNLEREC
VEETCSYEEAFEALESSTATDVFWAKYTACETARTPRDKLAACLEGNCAEGLGTNYRGHV
NITRSGIECQLWRSRYPHKPEINSTTHPGADLQENFCRNPDSSTTGPWCYTTDPTVRRQE
CSIPVCGQDQVTVAMTPRSEGSSVNLSPPLEQCVPDRGQQYQGRLAVTTHGLPCLAWASA
QAKALSKHQDFNSAVQLVENFCRNPDGDEEGVWCYVAGKPGDFGYCDLNYCEEAVEEETG
DGLDEDSDRAIEGRTATSEYQTFFNPRTFGSGEADCGLRPLFEKKSLEDKTERELLESYI
DGRIVEGSDAEIGMSPWQVMLFRKSPQELLCGASLISDRWVLTAAHCLLYPPWDKNFTEN
DLLVRIGKHSRTRYERNIEKISMLEKIYIHPRYNWRENLDRDIALMKLKKPVAFSDYIHP
VCLPDRETAASLLQAGYKGRVTGWGNLKETWTANVGKGQPSVLQVVNLPIVERPVCKDST
RIRITDNMFCAGYKPDEGKRGDACEGDSGGPFVMKSPFNNRWYQMGIVSWGEGCDRDGKY
GFYTHVFRLKKWIQKVIDQFGE

Already parsed 1 XML elements.
'''
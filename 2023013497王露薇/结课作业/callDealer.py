#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys


def dealwithElement(elem, tag_name):
    """Function to process each XML element"""
    if isinstance(elem, object):
        if tag_name == "sequence":
            # For sequence tag, print text directly (keep original format)
            print(elem.text)
        else:
            # For other tags (like accession), add tag name prefix
            print(f"{tag_name}: {elem.text}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer.py <xml_file> <elemTag>")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    # 使用装饰器包装处理函数
    wrapped_func = largeXMLDealer.largeXMLDealer.parse_decorator(elemTag=elemTag)(
        lambda elem: dealwithElement(elem, elemTag))
    wrapped_func(fileName)

'''
CALL EXAMPLE 1:
COMMAND LINE:     python3 callDealer.py P00734.xml accession
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
COMMAND LINE:     python3 callDealer.py P00734.xml sequence
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

#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys
#!/usr/bin/env python
# coding:utf-8

from largeXMLDealer import XMLDealer
import sys

@XMLDealer
def dealwithElement(elem):
    """处理每个 XML 元素"""
    if elem.text is not None:
        print(elem.text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer.py <xml_file> <tag>")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    dealwithElement(fileName, elemTag)
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

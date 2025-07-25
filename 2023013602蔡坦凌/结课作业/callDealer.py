#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys

@largeXMLDealer.XMLDecorator
def dealwithElement(elem):
    """"""
    if isinstance(elem, object):
        print(elem.text)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        fileName = sys.argv[1]
        elemTag = sys.argv[2]

        lxmld = largeXMLDealer.largeXMLDealer()
        decorator = largeXMLDealer.XMLDecorator(dealwithElement)
        count = lxmld.parse(fileName, elemTag, decorator)
        print("Already parsed %d XML elements." % decorator.get_count())
    else:
        print("Usage: python3 callDealer.py <filename> <tag>")

'''
CALL EXAMPLE 1:
COMMAND LINE:     python theLastWork/callDealer.py theLastWork/P00734.xml accession
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
COMMAND LINE:     python theLastWork/callDealer.py theLastWork/P00734.xml sequence 
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
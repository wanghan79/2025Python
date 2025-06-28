#!/usr/bin/env python
# coding:utf-8

from largeXMLDealer import largeXMLDealer
import sys


@largeXMLDealer
def dealwithElement(elem):
    """处理XML元素，打印元素文本内容"""
    if isinstance(elem, object):
        print(elem.text)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python ./callDealer.py [XML文件] [元素标签]")
        sys.exit(1)
        
    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    # 调用被装饰后的函数
    count = dealwithElement(fileName, elemTag)
    print("已解析 %d 个XML元素。" % count)

'''
调用示例 1:
命令行:     python callDealer.py P00734.xml accession
输出:           
P00734
B2R7F7
B4E1A7
Q4QZ40
Q53H04
Q53H06
Q69EZ7
Q7Z7P3
Q9UCA1
已解析 9 个XML元素。          


调用示例 2:
命令行:     python callDealer.py P00734.xml sequence
输出:           
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

已解析 1 个XML元素。
'''

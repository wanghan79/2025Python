#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""
import os.path as path
from optparse import OptionParser
import xml.etree.ElementTree as etree

class LargeXMLParser:
    def __init__(self, filename, elemTag):
        self.filename = filename
        self.elemTag = elemTag

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                if not path.isfile(self.filename) or not self.filename.endswith("xml"):
                    raise FileNotFoundError(f"File not found or not a valid XML file: {self.filename}")

                count = 0
                es = ('end',)
                ns = self._getNamespace(self.filename)
                ns = f"{{{ns}}}"

                context = etree.iterparse(self.filename, events=es, tag=ns + self.elemTag)

                for event, elem in context:
                    try:
                        func(elem, **kwargs)
                    except Exception as e:
                        print(f"Error in the decorated function: {e}")
                    finally:
                        elem.clear()
                        count += 1
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]
                del context
                print(f"Parsed {count} XML elements.")
                return count
            except FileNotFoundError as e:
                print(f"File error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        return wrapper

    def _getNamespace(self, fileName):
        try:
            if not path.isfile(fileName) or not fileName.endswith("xml"):
                raise FileNotFoundError(f"File not found or not a valid XML file: {fileName}")
            result = ''
            es = ('start-ns',)
            context = etree.iterparse(fileName, events=es)
            for event, elem in context:
                prefix, result = elem
                break
            del context
            return result
        except FileNotFoundError as e:
            print(f"File error: {e}")
            return ''

def process_nested(elem, bPrint=True, outputFile=None):
    """递归处理子元素"""
    if bPrint:
        print(f"Processing Tag: {elem.tag}, Text: {elem.text}")
    if outputFile:
        outputFile.write(f"Tag: {elem.tag}, Text: {elem.text}\n")
    for child in elem:
        process_nested(child, bPrint=bPrint, outputFile=outputFile)

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False, action="store_true",
                      help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile", default=None,
                      help="Output the results to a file.")
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                      help="The XML tag interested to parse.")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception(f"The input file is not exist or a valid XML file: {filePath}")

    if options.outputFile:
        with open(options.outputFile, 'w') as output_file:
            @LargeXMLParser(filePath, options.tag)
            def dealwithElement(elem, bPrint=options.bPrint, outputFile=output_file):
                if bPrint:
                    print(f"Current Tag: {elem.tag}, Text: {elem.text}")
                if output_file:
                    output_file.write(f"Current Tag: {elem.tag}, Text: {elem.text}\n")
                process_nested(elem, bPrint=bPrint, outputFile=output_file)

            dealwithElement()
    else:
        @LargeXMLParser(filePath, options.tag)
        def dealwithElement(elem, bPrint=options.bPrint, outputFile=None):
            if bPrint:
                print(f"Current Tag: {elem.tag}, Text: {elem.text}")
            process_nested(elem, bPrint=bPrint, outputFile=outputFile)

        dealwithElement()

if __name__ == "__main__":
    main()
# Linux Command Line Example:
# python3 largeXMLDealer.py -t entry /home/Biodata/OrignalData/Protein/Uniprot/current/uniprot_sprot.xml

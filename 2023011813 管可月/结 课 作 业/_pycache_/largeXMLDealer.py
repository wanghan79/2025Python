#!/usr/bin/env python
# coding:utf-8
"""
Enhanced XML Parser for Files >500MB
Features:
- Stream processing with memory optimization
- Namespace auto-detection
- Multi-output support (print/file)
"""

from lxml import etree
from os import path
from optparse import OptionParser
import sys
import time

class LargeXMLDealer:
    def __init__(self):
        self.namespaces = {}

    def parse(self, fileName, elemTag, func4Element=None):
        # Validate input
        if not path.isfile(fileName):
            raise FileNotFoundError(f"File not found: {fileName}")
        if not fileName.lower().endswith(".xml"):
            raise ValueError("Input must be an XML file")

        # Detect namespaces
        self._detect_namespaces(fileName)
        full_tag = self._resolve_tag(elemTag)

        # Parse with progress
        count = 0
        start_time = time.time()
        context = etree.iterparse(fileName, events=("end",), tag=full_tag)

        for event, elem in context:
            try:
                if func4Element:
                    func4Element(elem)
            except Exception as e:
                sys.stderr.write(f"\nError processing element: {e}\n")
                raise
            finally:
                elem.clear()
                count += 1
                # Progress feedback
                if count % 1000 == 0:
                    sys.stderr.write(f"\rParsed {count} elements...")
                    sys.stderr.flush()

        sys.stderr.write(f"\nParsing completed in {time.time()-start_time:.2f}s\n")
        return count

    def _detect_namespaces(self, fileName):
        context = etree.iterparse(fileName, events=("start",))
        try:
            for event, elem in context:
                if hasattr(elem, 'nsmap'):
                    self.namespaces = elem.nsmap
                break  # Only check root element
        finally:
            del context

    def _resolve_tag(self, tag):
        if ':' in tag:
            prefix, name = tag.split(':')
            ns = self.namespaces.get(prefix)
            return f"{{{ns}}}{name}" if ns else tag
        else:
            ns = self.namespaces.get(None)
            return f"{{{ns}}}{tag}" if ns else tag

def main():
    usage = "Usage: %prog -t TAG [-p|-o FILE] INPUT_XML"
    parser = OptionParser(usage)
    parser.add_option("-t", "--tag", dest="tag",
                    help="XML tag to parse (e.g. 'entry' or 'ns:entry')", metavar="TAG")
    parser.add_option("-p", "--print", action="store_true", dest="print",
                    help="Print results to console")
    parser.add_option("-o", "--output", dest="output",
                    help="Output file path", metavar="FILE")

    options, args = parser.parse_args()

    # Validation
    if len(args) != 1:
        parser.error("Requires exactly 1 input file")
    if not options.tag:
        parser.error("Must specify target tag with -t")
    if options.print and options.output:
        parser.error("Cannot use -p and -o simultaneously")

    # Process
    processor = LargeXMLDealer()
    input_file = path.abspath(args[0])

    if options.print:
        def print_element(elem):
            print(etree.tostring(elem, encoding='unicode').strip())
        count = processor.parse(input_file, options.tag, print_element)
    elif options.output:
        elements = []
        def collect(elem):
            elements.append(etree.tostring(elem, encoding='unicode').strip())
        count = processor.parse(input_file, options.tag, collect)
        with open(options.output, 'w', encoding='utf-8') as f:
            f.write("\n".join(elements))
    else:
        count = processor.parse(input_file, options.tag)

    print(f"Total {count} elements processed", file=sys.stderr)

if __name__ == "__main__":
    main()
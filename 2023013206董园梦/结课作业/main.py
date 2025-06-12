"""
    author: Zhang Lizhi
    date: 2025.06.03
    name: 结课作业
    run: python main.py fileName elemTag
"""

import sys
from lxml import etree
from os import path
from functools import wraps

class XMLProcessor:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, file_name, element_tag):
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        events = ('end', )
        namespace = self._get_namespace(file_name)
        namespace = "{%s}" % namespace
        context = etree.iterparse(file_name, events=events, tag=namespace + element_tag)

        for event, element in context:
            try:
                self.func(element)
            except Exception as e:
                raise Exception(f"Error in function parameter: {e}")
            finally:
                element.clear()
                count += 1
                while element.getprevious() is not None:
                    del element.getparent()[0]
        del context
        return count

    def _get_namespace(self, file_name):
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")
        result = ''
        events = ('start-ns', )
        context = etree.iterparse(file_name, events=events)
        for event, elem in context:
            prefix, result = elem
            break
        del context
        return result

    def extract_structure(self, element):
        tag_counts = {}

        def _extract_structure(elem, level=0):
            nonlocal tag_counts
            tag = elem.tag
            if tag not in tag_counts:
                tag_counts[tag] = 0
            tag_counts[tag] += 1

            print("  " * level + f"<{tag}>")

            if elem.text and elem.text.strip():
                print("  " * (level + 1) + f"Text: {elem.text.strip()}")
            for child in elem:
                _extract_structure(child, level + 1)

            print("  " * level + f"</{tag}>")

        _extract_structure(element)

        print("\nTag counts:")
        for tag, count in tag_counts.items():
            print(f"{tag}: {count}")


@XMLProcessor
def process_element(element):
    processor = XMLProcessor(lambda x: None)
    processor.extract_structure(element)


if __name__ == "__main__":
    file_name = sys.argv[1]
    element_tag = sys.argv[2]
    count = process_element(file_name, element_tag)
    print(f"\nTotal number of '{element_tag}' tags: {count}")
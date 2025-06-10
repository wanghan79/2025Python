#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M using a decorator
  Created: 4/4/2016
"""

from lxml import etree
from os import path
from functools import wraps


def parse_large_xml(fileName, elemTag):

    if not path.isfile(fileName) or not fileName.endswith("xml"):
        raise FileNotFoundError(f"The file {fileName} does not exist or is not an XML file.")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            ns = _get_namespace(fileName)
            namespace_tag = f"{{{ns}}}{elemTag}" if ns else elemTag

            context = etree.iterparse(fileName, events=('end',), tag=namespace_tag)

            for event, elem in context:
                try:
                    func(elem, *args, **kwargs)
                except Exception as e:
                    raise RuntimeError(f"Error calling user-defined function on element: {e}")
                finally:
                    elem.clear()
                    count += 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            return count

        return wrapper

    return decorator


def _get_namespace(fileName):
    if not path.isfile(fileName) or not fileName.endswith("xml"):
        raise FileNotFoundError(f"The file {fileName} does not exist or is not an XML file.")

    result = ''
    context = etree.iterparse(fileName, events=('start-ns',))

    for event, elem in context:
        prefix, uri = elem
        result = uri
        break

    del context
    return result
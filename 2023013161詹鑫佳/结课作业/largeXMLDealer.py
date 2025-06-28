from lxml import etree
from os import path
from optparse import OptionParser

'''
原本是一个类方法 parse 用于解析 XML 文件，现在将其改为一个装饰器 __call__，
目的是让解析 XML 的功能可以通过修饰器修饰任意一个处理 XML 元素的函数。
'''

class largeXMLDealer:
    def __init__(self, fileName=None, elemTag=None):
        """
        初始化传入的 XML 文件路径 和 指定的标签 tag
        这部分替代原来的 parse 函数中的参数
        """
        self.fileName = fileName
        self.elemTag = elemTag

    def _getNamespace(self, fileName):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            break
        del context
        return result

    def __call__(self, func):
        """
        将类的实例变成装饰器，包装传入的函数 func
        功能与原 parse 函数完全一致：对每一个匹配的 elem 调用 func
        """

        def wrapper():
            if not path.isfile(self.fileName) or not self.fileName.endswith("xml"):
                raise FileNotFoundError
            count = 0
            es = ('end',)
            ns = "{%s}" % self._getNamespace(self.fileName)
            context = etree.iterparse(self.fileName, events=es, tag=ns + self.elemTag)

            for event, elem in context:
                try:
                    func(elem)
                except Exception as e:
                    raise Exception("Error in decorated function: %s" % str(e))
                finally:
                    elem.clear()
                    count += 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            print("Already parsed %d XML elements." % count)
        return wrapper


def main():
    """

    """
    # Construct the usage.
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False, action="store_true",
                      help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile", default=None,
                      help="Output the results to a file.")
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                      help="The XML tag interested to parse.")

    # Parse the options and args input by users.
    (options, args) = parser.parse_args()

    # Check the correction of users input and call the fuctions of class DoSomething.
    if (len(args) != 1):
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not exist or a vailable XML file.")
    # Call XML parser
    largXML = largeXMLDealer()
    count = largXML.parse(filePath, options.tag)
    print("Parsed %10d XML elements." % count)


if __name__ == "__main__":
    main()






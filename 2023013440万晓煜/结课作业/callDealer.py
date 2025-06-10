
import sys
from largeXMLDealer import largeXMLDealer



class ElementProcessorDecorator:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, elem):
        self.count += 1
        print(f"[第{self.count}个元素] <{elem.tag}>")

        if elem.text and elem.text.strip():
            print(f"内容: {elem.text.strip()}")
        else:
            for child in elem.iter():
                if child is not elem and child.text and child.text.strip():
                    print(f"子元素 <{child.tag}>: {child.text.strip()}")

        return self.func(elem)

@ElementProcessorDecorator
def dealwithElement(elem):
    pass  


if __name__ == "__main__":
    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    from largeXMLDealer import largeXMLDealer
    lxmld = largeXMLDealer(dealwithElement)
    count = lxmld(fileName, elemTag)

    print(f"已处理{count}个<{elemTag}>元素")

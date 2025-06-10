import sys
from largeXMLDealer import largeXMLDealer

@largeXMLDealer
def dealwithElement(elem):
    """被修饰函数：调用结构打印功能"""
    dealer = largeXMLDealer(lambda x: None)  
    dealer.extract_structure(elem)


if __name__ == "__main__":
    fileName = sys.argv[1]
    elemTag = sys.argv[2]
    count = dealwithElement(fileName, elemTag)
    print(f"共解析出{count}个<{elemTag}>元素")

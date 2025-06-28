import sys
from largeXMLDealer import largeXMLDealer
# 修改点：使用 largeXMLDealer 实例作为装饰器修饰 dealwithElement 函数
# 用装饰器来实现解析功能，从而取消了直接调用 parse 的过程

fileName = sys.argv[1]
elemTag = sys.argv[2]

# 使用 largeXMLDealer 作为装饰器：指定文件名和标签
@largeXMLDealer(fileName=fileName, elemTag=elemTag)
def dealwithElement(elem):
    if isinstance(elem, object):
        print(elem.text)

if __name__ == "__main__":
    dealwithElement()





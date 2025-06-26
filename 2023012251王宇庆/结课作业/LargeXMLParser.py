from lxml import etree
from os import path


class LargeXMLParser:
    """
    用于流式解析大型 XML 文件，节省内存并通过回调处理每个元素。
    """

    def __init__(self, target_tag=None, verbose=True):
        """
        :param target_tag: 指定要解析的标签（包含命名空间的完整标签或 None 处理所有）
        :param verbose: 是否打印调试信息
        """
        self.target_tag = target_tag
        self.verbose = verbose

    def parse(self, file_name, callback):
        """
        解析 XML 文件，每处理一个目标标签元素就调用一次 callback。
        :param file_name: XML 文件路径
        :param callback: 接收 etree.Element 的函数
        """
        if not path.isfile(file_name):
            self._log(f"[错误] 文件不存在: {file_name}")
            return

        count = 0

        try:
            context = etree.iterparse(file_name, events=('end',), recover=True)

            for _, elem in context:
                if self.target_tag is None or elem.tag.endswith(self.target_tag):
                    try:
                        callback(elem)
                        count += 1
                    except Exception as e:
                        self._log(f"[异常] 回调处理 <{elem.tag}> 时出错: {e}")

                # 内存清理
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

            del context
            self._log(f"[完成] 处理完成，解析元素总数: {count}")

        except etree.XMLSyntaxError as e:
            self._log(f"[XML 错误] 语法错误: {e}")
        except Exception as e:
            self._log(f"[异常] 解析过程出错: {e}")

    def _log(self, message):
        """内部日志输出控制"""
        if self.verbose:
            print(message)

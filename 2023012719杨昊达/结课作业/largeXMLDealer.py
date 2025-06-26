import os
import logging
from lxml import etree

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('largeXMLDealer')


class LargeXMLParser:
    """
    高效的大型XML文件解析器，使用迭代处理避免内存溢出
    """

    def __init__(self, max_element_size=10_000_000):
        """
        初始化解析器

        :param max_element_size: 单个元素最大允许大小（字节），防止异常大元素导致内存溢出
        """
        self.max_element_size = max_element_size

    def parse(self, file_path, element_processor, events=('end',),  ** kwargs):
        """
        迭代解析XML文件

        :param file_path: XML文件路径
        :param element_processor: 元素处理函数，接受element作为参数
        :param events: 监听的事件类型，默认为('end',)
        :param kwargs: 传递给lxml.iterparse的额外参数
        """
        if not os.path.isfile(file_path):
            logger.error(f"文件不存在: {file_path}")
            return

        # 使用with确保文件资源正确释放
        with open(file_path, 'rb') as f:
            file_size = os.path.getsize(file_path)
            logger.info(f"开始解析XML文件: {file_path} ({file_size / 1024 / 1024:.2f} MB)")

            try:
                context = etree.iterparse(f, events=events,  ** kwargs)

                for event, elem in context:
                    # 检查元素大小限制
                    if self.max_element_size and \
                            len(etree.tostring(elem)) > self.max_element_size:
                        logger.warning(f"元素过大跳过: {elem.tag} "
                                       f"(大小: {len(etree.tostring(elem)) // 1024} KB > "
                                       f"限制: {self.max_element_size // 1024} KB)")
                        elem.clear()
                        continue

                    try:
                        element_processor(elem)
                    except Exception as e:
                        logger.error(f"处理元素 {elem.tag} 时出错: {e}")

                    # 清理当前元素和之前的兄弟元素
                    elem.clear()
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]

                # 清除根元素
                del context

            except etree.XMLSyntaxError as e:
                logger.error(f"XML语法错误: {e}")
            except Exception as e:
                logger.error(f"解析错误: {e}")

        logger.info(f"XML文件解析完成: {file_path}")
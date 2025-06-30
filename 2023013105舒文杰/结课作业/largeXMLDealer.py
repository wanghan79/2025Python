# largeXMLDealer.py

from lxml import etree
import os

class XMLParserUtil: 
    """
    负责以迭代方式解析大型XML文件，并根据指定的XML标签提取或处理元素。
   
    """
    def __init__(self, xml_document_path):
        """
        初始化 XMLParserUtil 实例。
        :param xml_document_path: 待解析XML文件的完整路径。
        """
        if not os.path.isfile(xml_document_path):
            raise FileNotFoundError(f"指定的XML文档不存在: {xml_document_path}")
        self.xml_document_path = xml_document_path
        self.total_processed_nodes = 0 # 记录处理的元素总数

    def parse_and_handle_elements(self, target_node_name=None, element_callback=None):
        """
        迭代解析XML文件，并在遇到每个元素的结束标签时，检查是否匹配目标标签。
        如果匹配，则调用提供的回调函数。

        :param target_node_name: 要关注的XML节点名称（不含命名空间前缀）。
                                 如果为 None 或空字符串，则会对所有元素的结束标签进行处理。
        :param element_callback: 一个回调函数，它接受一个 lxml.etree.Element 对象作为参数。
                                 此函数将在每个匹配的元素上被调用。
        """
        print(f"正在启动XML文件解析器处理文件: '{self.xml_document_path}'...")
        if target_node_name:
            print(f"  配置为仅关注标签: '{target_node_name}'。")
        else:
            print("  配置为处理文档中的所有元素。")

        try:
            # 使用 iterparse 进行迭代解析，只监听 'end' 事件以确保整个元素已加载
            context_iterator = etree.iterparse(self.xml_document_path, events=('end',), recover=True)

            for _, current_element in context_iterator:
                # 提取不带命名空间前缀的本地标签名
                full_element_tag = current_element.tag
                local_tag = self._get_local_tag(full_element_tag)
                self.total_processed_nodes += 1

                # 检查元素是否匹配目标名称（如果指定了目标名称）
                if not target_node_name or local_tag == target_node_name:
                    if element_callback:
                        try:
                            # 调用外部提供的处理函数
                            element_callback(current_element)
                        except Exception as cb_err:
                            print(f"警告: 处理元素 <{full_element_tag}> 时回调函数遇到错误: {cb_err}")

                # 关键的内存管理：清除已处理元素的引用，防止内存累积
                self._release_element_memory(current_element)

            print(f"XML文件解析操作完成。共检查了 {self.total_processed_nodes} 个XML节点。")

        except etree.XMLSyntaxError as xml_err:
            print(f"错误: 解析XML文件时发现语法问题: {xml_err}")
        except Exception as general_err:
            print(f"解析和处理XML文件时发生未知错误: {general_err}")

    def _get_local_tag(self, full_qualified_tag):
        """
        从完整的（可能包含命名空间的）标签名中提取不带命名空间的部分。
        例如：'{http://uniprot.org/uniprot}sequence' -> 'sequence'
        """
        if '}' in full_qualified_tag:
            return full_qualified_tag.split('}', 1)[1]
        return full_qualified_tag

    def _release_element_memory(self, element_to_clear):
        """
        清理并移除元素的引用，以减少内存占用。
        此方法旨在协助 iterparse 的内存优化。
        """
        # 清除当前元素的子节点
        element_to_clear.clear()
        # 移除指向前一个兄弟节点的引用，以便垃圾回收
        parent = element_to_clear.getparent()
        if parent is not None:
            if element_to_clear.getprevious() is not None:
                del parent[0] # 删除第一个子节点，因为iterparse处理完毕的节点会被推到前面
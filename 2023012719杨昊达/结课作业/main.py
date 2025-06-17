import os
import logging
from functools import wraps
from lxml import etree
from largeXMLDealer import LargeXMLParser
import hashlib
import time

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('XMLProcessor')


FILE_PATH = os.path.join(os.path.dirname(__file__), "example.xml")
TARGET_TAGS = ['sequence', 'entry']  # 可以指定多个标签
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)



# 自定义处理函数

def get_tag_without_namespace(tag):
    """提取不带命名空间的标签名"""
    return tag.split('}', 1)[1] if '}' in tag else tag


def generate_unique_filename(content, prefix="seq"):
    """为序列内容生成唯一文件名"""
    # 使用哈希值确保文件名唯一
    hash_val = hashlib.md5(content.encode('utf-8')).hexdigest()
    return f"{prefix}_{hash_val[:8]}.txt"


def process_element(elem):
    """
    实际处理XML元素的函数，可以根据需要定制
    """
    # 提取标签名称（不含命名空间）
    tag = get_tag_without_namespace(elem.tag)

    # 根据标签类型执行不同处理
    if tag == 'sequence':
        # 处理sequence元素
        text = elem.text.strip() if elem.text else ''
        if not text:
            logger.warning("发现空序列内容，跳过保存")
            return

        seq_id = elem.get('id', '')
        if not seq_id:
            # 尝试从上级元素中获取ID
            parent = elem.getparent()
            if parent is not None:
                if parent.get('id'):
                    seq_id = f"{parent.get('id')}_seq"
                elif parent.findtext('{*}accession'):
                    seq_id = f"{parent.findtext('{*}accession')}_seq"

            # 如果还是没有ID，生成唯一文件名
            if not seq_id:
                logger.info("序列没有ID属性，将生成唯一文件名")
                seq_id = generate_unique_filename(text)

        logger.info(f"发现序列: ID={seq_id}, 长度={len(text)}")

        # 为序列生成文件名
        filepath = os.path.join(OUTPUT_DIR, f"{seq_id}.txt")

        # 将序列保存到文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            logger.info(f"序列已保存至: {filepath}")
        except Exception as e:
            logger.error(f"保存序列文件失败: {e}")

    elif tag == 'entry':
        # 处理entry元素
        accession = elem.findtext('{*}accession')
        protein_name = elem.findtext('{*}protein/{*}recommendedName/{*}fullName')

        if accession and protein_name:
            logger.info(f"处理蛋白质条目: {accession} - {protein_name}")
        else:
            if not accession:
                logger.warning("entry元素缺少accession信息")
            if not protein_name:
                logger.warning("entry元素缺少protein名称信息")

    elif tag == 'feature':
        # 处理feature元素
        feature_type = elem.get('type')
        location = elem.findtext('{*}location')
        logger.debug(f"发现特征: 类型={feature_type}, 位置={location}")

    else:
        logger.debug(f"处理其他标签元素: {tag}")



# 解析器装饰器

def xml_parser_decorator(file_path, target_tags=None):
    """
    创建XML解析器装饰器

    :param file_path: XML文件路径
    :param target_tags: 要处理的标签列表（None表示所有标签）
    :return: 装饰器函数
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建解析器实例
            parser = LargeXMLParser(max_element_size=5_000_000)

            def element_processor(elem):
                # 提取标签名称（不含命名空间）
                tag = get_tag_without_namespace(elem.tag)

                # 检查是否匹配目标标签
                if target_tags is None or tag in target_tags:
                    logger.debug(f"处理匹配元素: <{tag}>")
                    try:
                        func(elem, *args, **kwargs)
                    except Exception as e:  # 修复：移除多余的缩进
                        logger.error(f"处理元素失败: {tag}: {e}")  # 修复：添加到except块中

            # 开始解析
            parser.parse(file_path, element_processor,
                         remove_blank_text=True,  # 节省内存
                         remove_comments=True)  # 节省内存

        return wrapper

    return decorator



# 主处理流程

@xml_parser_decorator(file_path=FILE_PATH, target_tags=TARGET_TAGS)
def process_target_elements(elem):
    """
    被装饰的函数，实际处理匹配的元素
    """
    process_element(elem)


if __name__ == "__main__":
    logger.info(f"开始处理XML文件: {FILE_PATH}")
    logger.info(f"目标标签: {TARGET_TAGS or '所有标签'}")

    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 清理可能存在的旧输出（可选）
    for file in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, file))

    start_time = time.time()
    process_target_elements()
    elapsed_time = time.time() - start_time

    # 检查输出目录内容
    output_files = os.listdir(OUTPUT_DIR)
    logger.info(f"输出目录文件数量: {len(output_files)}")
    if output_files:
        logger.info(f"输出文件示例: {output_files[:3]}{'...' if len(output_files) > 3 else ''}")

    logger.info(f"XML处理完成，耗时: {elapsed_time:.2f}秒")

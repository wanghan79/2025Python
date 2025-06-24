import largeXMLDealer
import sys
from typing import Optional
import logging
from pathlib import Path

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def display_element_content(element, max_length: int = 100) -> None:
    """
    显示XML元素内容，带截断处理

    Args:
        element: XML元素对象
        max_length: 最大显示长度
    """
    if element.text and (content := element.text.strip()):
        display_text = content if len(content) <= max_length else f"{content[:max_length]}..."
        print(display_text)


def validate_file_path(file_path: str) -> bool:
    """
    验证文件路径是否存在且是XML文件

    Args:
        file_path: 文件路径字符串

    Returns:
        bool: 路径是否有效
    """
    path = Path(file_path)
    return path.exists() and path.is_file() and path.suffix.lower() == '.xml'


def get_user_input(prompt: str, validation_func: Optional[callable] = None) -> str:
    """
    获取并验证用户输入

    Args:
        prompt: 提示信息
        validation_func: 验证函数

    Returns:
        验证通过的用户输入
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("输入不能为空")

            if validation_func and not validation_func(user_input):
                raise ValueError("无效的输入")

            return user_input
        except ValueError as e:
            logger.error(f"输入错误: {e}")
            print("请重新输入...")


def parse_xml_file(file_path: str, target_tag: str) -> None:
    """
    解析XML文件并处理指定标签

    Args:
        file_path: XML文件路径
        target_tag: 要解析的XML标签名
    """

    @largeXMLDealer.xml_parser(file_path, target_tag)
    def process_element(element):
        display_element_content(element)

    try:
        logger.info(f"开始解析文件: {file_path}，目标标签: {target_tag}")
        process_element()
        logger.info("XML解析完成")
    except Exception as e:
        logger.error(f"解析XML时出错: {e}")
        sys.exit(1)


def main() -> None:
    """
    主程序入口
    """
    print("XML文件解析工具")
    print("=" * 30)

    # 获取用户输入
    xml_file = get_user_input(
        "请输入XML文件路径: ",
        validate_file_path
    )
    xml_tag = get_user_input(
        "请输入要解析的XML标签名: ",
        lambda x: len(x) > 0
    )

    # 解析XML文件
    parse_xml_file(xml_file, xml_tag)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"程序异常: {e}")
        sys.exit(1)
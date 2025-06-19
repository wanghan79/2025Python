#大型 XML 文件处理工具说明文档

这个工具旨在处理大型 XML 文件，具备解析特定标签内容和分析 XML 文件完整结构的功能。


##一、功能特性：
1.解析特定标签：从大型 XML 文件中提取指定标签的内容。
2.分析 XML 结构：分析 XML 文件的完整结构，包含层级关系和最大深度。



##二、使用步骤及命令演示：
###1.安装依赖：
本工具依赖 lxml 库，可使用以下命令进行安装：
pip install lxml

###2.解析特定标签：
`python callDealer.py <xml_file> <elem_tag> [--output <output_file>] [--verbose]`
<xml_file>：待处理的 XML 文件路径。
<elem_tag>：要解析的元素标签名，例如 accession。
--output <output_file>：将结果输出到指定文件，而非控制台。
--verbose：显示详细处理信息。

示例：`python callDealer.py P00734.xml accession --output result.txt --verbose`


3.分析 XML 结构：
`python callDealer.py <xml_file> --analyze [--output <output_file>] [--verbose]`
<xml_file>：待处理的 XML 文件路径。
--analyze：分析 XML 文件的完整结构。
--output <output_file>：将结果输出到指定文件，而非控制台。
--verbose：显示详细处理信息。

示例：`python callDealer.py big_data.xml --analyze --output structure.txt --verbose`



三、可能的输出结果样例
1.解析特定标签：
若解析 accession 标签，输出可能如下：
`P00734
P01234
P02345`

2.分析 XML 结构：
分析结果将以树形结构展示 XML 的层级关系，示例如下：
`============================================================
XML结构分析结果 - 文件: big_data.xml
============================================================

发现 1 个根节点:
  - root
    ├── child1
    │   ├── grandchild1
    │   └── grandchild2
    └── child2
        └── grandchild3

最大层级深度: 3
============================================================`



四、注意事项
1.请确保输入的 XML 文件存在且格式正确。
2.若使用 --output 选项，请确保有足够的权限创建和写入文件。
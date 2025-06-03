# 课程作业Readme


姓名：张高升
学号：2023013322


## 作业一：银行家算法实现

本作业侧重于在操作系统中实现银行家算法以避免死锁。

### 文件

  * `banker.py`: 包含银行家算法的核心功能。
      * `safety_check(**kwargs)`: 检查系统是否处于安全状态，返回一个布尔值和安全序列（如果存在）。
      * `banker_algorithm(**kwargs)`: 模拟资源请求，判断是否可以安全地批准请求，并相应地更新系统状态。
      * `print_matrix(**kwargs)`: 一个辅助函数，用于以可读格式打印矩阵。
  * `main.py`: 通过模拟资源请求并打印请求前后系统状态来演示银行家算法的使用。

### 如何运行

要运行银行家算法模拟，请执行 `main.py`：

```bash
python main.py
```

输出将显示初始系统状态、安全检查的结果，以及模拟资源请求的结果，包括如果请求被批准则更新后的矩阵。

## 作业二：随机样本生成

本作业涉及使用 Python 生成器创建灵活的随机样本生成器。

### 文件

  * `RandomSample.py`: 实现根据提供的结构随机生成各种数据类型（字符串、整数、浮点数、列表、字典、元组）的函数。
      * `gen_str(data)`: 生成一个随机字符串。
      * `gen_int(data)`: 生成一个随机整数。
      * `gen_float(data)`: 生成一个随机浮点数。
      * `gen_list(data)`: 生成随机样本列表。
      * `gen_dict(data)`: 生成随机样本字典。
      * `gen_tuple(data)`: 生成随机样本元组。
      * `generate_sample(struct)`: 根据给定结构递归生成样本。
      * `random_sampler(**kwargs)`: 一个生成器函数，生成指定数量的随机样本。

### 如何运行

要测试随机样本生成器，请执行 `RandomSample.py`：

```bash
python RandomSample.py
```

脚本将根据文件中定义的 `example` 结构生成并打印指定数量的随机样本。

## 作业三：用于统计操作的装饰器

本作业通过添加一个参数化装饰器来增强随机样本生成功能，以实现统计分析。

### 文件

  * `Decorator.py`: 包含作业二中的随机样本生成函数，并增加了装饰器以对生成的数值数据执行统计操作。
      * `extract_int(data)`: 从可能嵌套的数据结构中提取所有数值（整数和浮点数）。
      * `StaticsResInt(**vargs)`: 一个装饰器，用于计算和打印从生成的样本中提取的数值数据的统计信息（SUM、AVG、VAR、RMSE）。
      * `random_sampler(**kwargs)`: 经过装饰的生成器函数，用于生成随机样本。

### 如何运行

要运行带装饰器的随机样本生成器，请执行 `Decorator.py`：

```bash
python Decorator.py
```

脚本将生成样本，打印它们，然后显示这些样本中数值的计算统计信息（SUM、AVG、VAR、RMSE）。可以更换装饰器的参数以获取不同的统计信息。

## 结课作业：大型 XML 文件解析器

本项目演示了如何使用 Python 高效地解析大型 XML 文件，特别关注于迭代处理。它包含一个核心类 `largeXMLDealer`，用于逐元素解析 XML，以及一个示例 `main.py`，展示了如何使用该类来提取和处理特定标签的数据。

### 项目结构

```
结课作业/
├── example.xml         # (大型)示例 XML 文件 (UniProt 数据)
├── largeXMLDealer.py   # 包含 largeXMLDealer 类的模块
└── main.py             # 使用 largeXMLDealer 解析 example.xml 的主脚本
```

### 文件说明

#### `largeXMLDealer.py`

这个模块定义了 `largeXMLDealer` 类，其主要功能如下：

- **初始化**: 构造函数 `__init__`。
- **解析**: `parse(fileName, func_for_element)` 方法。
    - 接收一个 XML 文件名和一个回调函数作为参数。
    - 使用 `lxml.etree.iterparse` 进行迭代解析，以事件驱动的方式处理 XML 元素，这对于大型文件非常重要，因为它避免了将整个文件加载到内存中。
    - 当遇到每个元素的结束标签时，调用 `func_for_element` 回调函数，并将当前元素传递给它。
    - 在处理完每个元素后，通过 `elem.clear()` 清理元素，以释放内存。
    - 包含错误处理机制，用于处理文件不存在、XML 语法错误以及回调函数执行期间的异常。

#### `main.py`

这个脚本演示了如何使用 `largeXMLDealer` 来解析 `结课作业/example.xml` 文件。

- **常量**:
    - `fileName`: 指向 `结课作业/example.xml` 的路径。
    - `elemTag`: 指定要处理的 XML 元素的标签名 (例如, `'sequence'`)。如果设置为 `None`，则会处理所有标签。
- **装饰器 `largeXMLparse(file_name, element_tag)`**:
    - 这是一个工厂函数，返回一个装饰器。
    - 该装饰器接收一个函数作为参数 (即被修饰的函数)。
    - 在内部，它实例化 `largeXMLDealer`。
    - 它定义了一个回调函数 `element_processor_callback`，此回调函数会传递给 `largeXMLDealer` 的 `parse` 方法。
    - `element_processor_callback` 负责检查当前处理的元素标签是否与 `element_tag` (如果提供)匹配。它能正确处理带有命名空间的标签 (例如 `{http://uniprot.org/uniprot}sequence` 会被正确匹配为 `sequence`)。
    - 如果标签匹配 (或者 `element_tag` 为 `None`)，则调用被修饰的函数，并将当前元素传递给它。
- **函数 `output(elem)`**:
    - 这个函数被 `@largeXMLparse` 装饰器修饰。
    - 它接收一个 XML 元素作为参数。
    - 它的作用是打印出找到的元素的标签和内容 (使用 `etree.tostring` 进行格式化输出)。
- **主执行块 (`if __name__ == "__main__":`)**:
    - 当脚本直接运行时，它会调用 `output()` 函数。由于 `output` 被装饰过，这将触发 `largeXMLDealer` 对 `example.xml` 的解析过程，并针对 `elemTag` 指定的标签调用 `output` 函数。

#### `example.xml`

一个位于 `结课作业/` 目录下的体积较大的 XML 文件，来自 UniProt 数据库，用作解析器处理大型数据集能力的示例。

### 如何运行 (结课作业)

1.  **修改参数 (可选)**:
    -   在 `结课作业/main.py` 中，您可以更改 `fileName` 变量来指向不同的 XML 文件。
    -   在 `结课作业/main.py` 中，您可以更改 `elemTag` 变量来指定您希望提取和处理的 XML 元素的特定标签名。如果将其设置为 `None`，脚本将处理 XML 文件中的所有元素。

2.  进入 `结课作业` 目录，然后执行：
    ```bash
    python main.py
    ```
    脚本将开始解析指定的 XML 文件，并根据 `elemTag` 的设置打印出匹配元素的信息。
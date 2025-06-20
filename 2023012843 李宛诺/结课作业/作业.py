import csv
import json
from typing import Iterator, Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@dataclass
class CSVConfig:
    """CSV配置类"""
    encoding: str = 'utf-8'
    delimiter: str = ','
    quotechar: str = '"'
    skip_empty_rows: bool = True
    lowercase_headers: bool = True
    strip_values: bool = True


class CSVProcessor:
    """CSV处理器类装饰器"""

    def __init__(self, filepath: str, config: Optional[CSVConfig] = None,
                 use_generator: bool = True, cache_data: bool = False):
        """
        初始化CSV处理器

        参数:
            filepath: CSV文件路径
            config: CSV配置对象
            use_generator: 是否使用生成器模式（适合大文件）
            cache_data: 是否缓存数据
        """
        self.filepath = Path(filepath)
        self.config = config or CSVConfig()
        self.use_generator = use_generator
        self.cache_data = cache_data
        self._cached_data = None

    def __call__(self, cls):
        """装饰器调用方法"""
        original_init = cls.__init__
        processor = self

        def new_init(instance, *args, **kwargs):
            # 调用原始初始化方法
            original_init(instance, *args, **kwargs)

            # 添加CSV处理相关的属性和方法
            instance._csv_processor = processor
            instance._data_iterator = None
            instance._raw_data = None

            # 自动加载数据
            if processor.use_generator:
                instance._data_iterator = processor._read_csv_generator()
            else:
                instance._raw_data = list(processor._read_csv_generator())

            # 添加便捷方法
            instance.get_data = lambda: processor._get_data(instance)
            instance.reload_data = lambda: processor._reload_data(instance)
            instance.export_json = lambda output_path: processor._export_json(instance, output_path)
            instance.get_column_stats = lambda column: processor._get_column_stats(instance, column)

        cls.__init__ = new_init
        return cls

    def _read_csv_generator(self) -> Iterator[Dict[str, Any]]:
        """生成器方式读取CSV"""
        if not self.filepath.exists():
            logging.error(f"文件不存在: {self.filepath}")
            return

        try:
            with open(self.filepath, 'r', encoding=self.config.encoding) as file:
                reader = csv.DictReader(
                    file,
                    delimiter=self.config.delimiter,
                    quotechar=self.config.quotechar
                )

                # 处理表头
                if self.config.lowercase_headers and reader.fieldnames:
                    reader.fieldnames = [field.lower().strip() for field in reader.fieldnames]

                logging.info(f"开始读取文件: {self.filepath}")
                logging.info(f"列名: {reader.fieldnames}")

                row_count = 0
                for row in reader:
                    # 跳过空行
                    if self.config.skip_empty_rows and not any(row.values()):
                        continue

                    # 清理数据
                    if self.config.strip_values:
                        row = {k: v.strip() if v else v for k, v in row.items()}

                    row_count += 1
                    yield row

                logging.info(f"成功读取 {row_count} 行数据")

        except Exception as e:
            logging.error(f"读取CSV文件失败: {e}")
            raise

    def _get_data(self, instance) -> List[Dict[str, Any]]:
        """获取数据（根据模式返回生成器或列表）"""
        if self.use_generator:
            return list(instance._data_iterator) if instance._data_iterator else []
        return instance._raw_data or []

    def _reload_data(self, instance):
        """重新加载数据"""
        if self.use_generator:
            instance._data_iterator = self._read_csv_generator()
        else:
            instance._raw_data = list(self._read_csv_generator())
        logging.info("数据已重新加载")

    def _export_json(self, instance, output_path: str):
        """导出数据为JSON"""
        data = self._get_data(instance)
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logging.info(f"数据已导出到: {output_file}")

    def _get_column_stats(self, instance, column: str) -> Dict[str, Any]:
        """获取指定列的统计信息"""
        data = self._get_data(instance)
        values = []

        for row in data:
            if column in row and row[column]:
                try:
                    values.append(float(row[column]))
                except ValueError:
                    pass

        if not values:
            return {"error": f"列 '{column}' 没有有效的数值数据"}

        return {
            "column": column,
            "count": len(values),
            "sum": sum(values),
            "average": sum(values) / len(values),
            "max": max(values),
            "min": min(values)
        }


# 数据验证装饰器（可链式使用）
def validate_data(validation_rules: Dict[str, Callable]):
    """数据验证装饰器"""

    def decorator(method):
        def wrapper(self, *args, **kwargs):
            data = self.get_data()
            invalid_rows = []

            for i, row in enumerate(data):
                for field, rule in validation_rules.items():
                    if field in row and not rule(row[field]):
                        invalid_rows.append((i + 1, field, row[field]))

            if invalid_rows:
                logging.warning(f"发现 {len(invalid_rows)} 个无效数据")
                for row_num, field, value in invalid_rows[:5]:  # 只显示前5个
                    logging.warning(f"行 {row_num}, 字段 '{field}': {value}")

            return method(self, *args, **kwargs)

        return wrapper

    return decorator


# 性能监控装饰器
def monitor_performance(method):
    """监控方法执行性能"""

    def wrapper(self, *args, **kwargs):
        start_time = datetime.now()
        result = method(self, *args, **kwargs)
        end_time = datetime.now()

        execution_time = (end_time - start_time).total_seconds()
        logging.info(f"{method.__name__} 执行时间: {execution_time:.2f} 秒")

        return result

    return wrapper


# ========== 使用示例 ==========

# 示例1：产品分析类
@CSVProcessor('data/products.csv', config=CSVConfig(delimiter=','))
class ProductAnalyzer:
    """产品数据分析器"""

    def __init__(self):
        self.analysis_results = {}

    @monitor_performance
    def analyze_price_distribution(self) -> Dict[str, int]:
        """分析价格分布"""
        data = self.get_data()
        price_ranges = {
            "0-50": 0,
            "50-100": 0,
            "100-200": 0,
            "200+": 0
        }

        for row in data:
            try:
                price = float(row.get('price', 0))
                if price < 50:
                    price_ranges["0-50"] += 1
                elif price < 100:
                    price_ranges["50-100"] += 1
                elif price < 200:
                    price_ranges["100-200"] += 1
                else:
                    price_ranges["200+"] += 1
            except ValueError:
                continue

        self.analysis_results['price_distribution'] = price_ranges
        return price_ranges

    @validate_data({'price': lambda x: x and float(x) > 0})
    def get_top_products(self, n: int = 5) -> List[Dict]:
        """获取价格最高的N个产品"""
        data = self.get_data()
        sorted_products = sorted(
            data,
            key=lambda x: float(x.get('price', 0)),
            reverse=True
        )
        return sorted_products[:n]


# 示例2：订单处理类（使用生成器模式）
@CSVProcessor('data/orders.csv', use_generator=True)
class OrderProcessor:
    """订单处理器 - 适合处理大文件"""

    def __init__(self):
        self.processed_count = 0

    def process_orders_in_batches(self, batch_size: int = 100):
        """批量处理订单"""
        batch = []

        # 重新加载数据以使用生成器
        self.reload_data()

        for row in self._data_iterator:
            batch.append(row)

            if len(batch) >= batch_size:
                self._process_batch(batch)
                batch = []

        # 处理剩余的数据
        if batch:
            self._process_batch(batch)

        logging.info(f"总共处理了 {self.processed_count} 个订单")

    def _process_batch(self, batch: List[Dict]):
        """处理一批订单"""
        # 这里可以添加实际的批处理逻辑
        self.processed_count += len(batch)
        logging.info(f"处理批次: {len(batch)} 个订单")


# 示例3：员工数据管理类
@CSVProcessor('data/employees.csv', cache_data=True)
class EmployeeManager:
    """员工数据管理器"""

    def __init__(self):
        self.departments = set()

    @monitor_performance
    def group_by_department(self) -> Dict[str, List[Dict]]:
        """按部门分组员工"""
        data = self.get_data()
        grouped = {}

        for employee in data:
            dept = employee.get('department', 'Unknown')
            self.departments.add(dept)

            if dept not in grouped:
                grouped[dept] = []
            grouped[dept].append(employee)

        return grouped

    def calculate_department_stats(self) -> Dict[str, Dict]:
        """计算各部门统计信息"""
        grouped = self.group_by_department()
        stats = {}

        for dept, employees in grouped.items():
            salaries = []
            for emp in employees:
                try:
                    salaries.append(float(emp.get('salary', 0)))
                except ValueError:
                    continue

            if salaries:
                stats[dept] = {
                    'employee_count': len(employees),
                    'avg_salary': sum(salaries) / len(salaries),
                    'max_salary': max(salaries),
                    'min_salary': min(salaries),
                    'total_salary': sum(salaries)
                }

        return stats


# 创建测试数据
def create_sample_data():
    """创建示例CSV文件"""
    import os
    os.makedirs('data', exist_ok=True)

    # 产品数据
    with open('data/products.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['product_id', 'name', 'price', 'category'])
        writer.writerows([
            ['P001', 'Laptop', '899.99', 'Electronics'],
            ['P002', 'Mouse', '29.99', 'Accessories'],
            ['P003', 'Keyboard', '79.99', 'Accessories'],
            ['P004', 'Monitor', '299.99', 'Electronics'],
            ['P005', 'Headphones', '149.99', 'Audio']
        ])

    # 员工数据
    with open('data/employees.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['employee_id', 'name', 'department', 'salary'])
        writer.writerows([
            ['E001', '张三', 'IT', '8000'],
            ['E002', '李四', 'HR', '6500'],
            ['E003', '王五', 'IT', '9000'],
            ['E004', '赵六', 'Sales', '7000'],
            ['E005', '钱七', 'IT', '8500']
        ])


# 主程序
if __name__ == "__main__":
    # 创建测试数据
    create_sample_data()

    print("\n" + "=" * 60)
    print("示例1: 产品分析")
    print("=" * 60)

    # 使用产品分析器
    analyzer = ProductAnalyzer()

    # 分析价格分布
    distribution = analyzer.analyze_price_distribution()
    print("\n价格分布:")
    for range_name, count in distribution.items():
        print(f"  {range_name}: {count} 个产品")

    # 获取价格最高的产品
    top_products = analyzer.get_top_products(3)
    print("\n价格最高的3个产品:")
    for product in top_products:
        print(f"  {product['name']}: ${product['price']}")

    # 导出为JSON
    analyzer.export_json('output/products_analysis.json')

    print("\n" + "=" * 60)
    print("示例2: 员工管理")
    print("=" * 60)

    # 使用员工管理器
    manager = EmployeeManager()

    # 部门统计
    dept_stats = manager.calculate_department_stats()
    print("\n部门统计信息:")
    for dept, stats in dept_stats.items():
        print(f"\n{dept} 部门:")
        print(f"  员工数: {stats['employee_count']}")
        print(f"  平均工资: ￥{stats['avg_salary']:.2f}")
        print(f"  最高工资: ￥{stats['max_salary']:.2f}")
        print(f"  最低工资: ￥{stats['min_salary']:.2f}")

    # 获取工资列统计
    salary_stats = manager.get_column_stats('salary')
    print(f"\n工资列统计: {salary_stats}")
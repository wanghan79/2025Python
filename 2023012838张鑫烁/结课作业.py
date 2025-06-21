import csv
import json
from functools import wraps
from typing import List, Dict, Any, Callable
import os

def csv_parser(filepath: str, encoding: str = 'utf-8', delimiter: str = ','):
    """
    CSV解析装饰器 - 负责主要的通用工作（文件解析）
    
    参数:
        filepath: CSV文件路径
        encoding: 文件编码，默认utf-8
        delimiter: 分隔符，默认逗号
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 装饰器做主要工作：解析CSV文件
            try:
                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"文件不存在: {filepath}")
                
                data = []
                with open(filepath, 'r', encoding=encoding) as file:
                    csv_reader = csv.DictReader(file, delimiter=delimiter)
                    
                    # 打印文件信息
                    print(f"正在解析CSV文件: {filepath}")
                    print(f"字段名: {csv_reader.fieldnames}")
                    print("-" * 60)
                    
                    # 读取所有数据
                    for row in csv_reader:
                        data.append(row)
                
                print(f"成功解析 {len(data)} 条记录")
                print("=" * 60)
                
                # 将解析后的数据传给被修饰函数处理
                # 这里体现了"反向"思想：装饰器产生数据，函数消费数据
                return func(data, *args, **kwargs)
                
            except Exception as e:
                print(f"CSV解析错误: {e}")
                return None
        
        return wrapper
    return decorator


# 示例1：统计分析函数（类似作业三的统计功能）
@csv_parser('data/sales.csv')
def analyze_sales_data(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """对销售数据进行统计分析"""
    print("销售数据统计分析")
    print("-" * 30)
    
    # 提取销售额数据
    sales_amounts = []
    for row in data:
        try:
            amount = float(row.get('amount', 0))
            sales_amounts.append(amount)
        except ValueError:
            continue
    
    if not sales_amounts:
        print("没有有效的销售数据")
        return {}
    
    # 进行统计计算（类似作业三的SUM、AVG、MAX、MIN）
    stats = {
        'SUM': sum(sales_amounts),
        'AVG': sum(sales_amounts) / len(sales_amounts),
        'MAX': max(sales_amounts),
        'MIN': min(sales_amounts),
        'COUNT': len(sales_amounts)
    }
    
    # 输出统计结果
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")
    
    return stats


# 示例2：数据筛选函数
@csv_parser('data/students.csv', encoding='utf-8')
def filter_excellent_students(data: List[Dict[str, Any]], threshold: float = 85.0) -> List[Dict]:
    """筛选优秀学生（成绩高于阈值）"""
    print(f"筛选成绩高于 {threshold} 的学生")
    print("-" * 30)
    
    excellent_students = []
    for student in data:
        try:
            score = float(student.get('score', 0))
            if score >= threshold:
                excellent_students.append(student)
                print(f"姓名: {student.get('name', 'Unknown')}, 成绩: {score}")
        except ValueError:
            continue
    
    print(f"\n共找到 {len(excellent_students)} 名优秀学生")
    return excellent_students


# 示例3：数据转换函数
@csv_parser('data/products.csv')
def export_to_json(data: List[Dict[str, Any]], output_file: str = 'output.json') -> None:
    """将CSV数据转换为JSON格式"""
    print(f"将数据转换为JSON格式")
    print("-" * 30)
    
    # 数据预处理
    processed_data = []
    for item in data:
        # 转换数值类型
        try:
            if 'price' in item:
                item['price'] = float(item['price'])
            if 'quantity' in item:
                item['quantity'] = int(item['quantity'])
        except ValueError:
            pass
        processed_data.append(item)
    
    # 保存为JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    
    print(f"成功导出 {len(processed_data)} 条记录到 {output_file}")


# 示例4：数据聚合函数
@csv_parser('data/orders.csv')
def aggregate_by_category(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """按类别聚合订单数据"""
    print("按类别聚合订单数据")
    print("-" * 30)
    
    category_stats = {}
    
    for order in data:
        category = order.get('category', 'Unknown')
        amount = float(order.get('amount', 0))
        
        if category not in category_stats:
            category_stats[category] = {
                'total': 0,
                'count': 0,
                'max': amount,
                'min': amount
            }
        
        stats = category_stats[category]
        stats['total'] += amount
        stats['count'] += 1
        stats['max'] = max(stats['max'], amount)
        stats['min'] = min(stats['min'], amount)
    
    # 计算平均值并输出
    for category, stats in category_stats.items():
        stats['average'] = stats['total'] / stats['count'] if stats['count'] > 0 else 0
        print(f"\n类别: {category}")
        print(f"  总额: {stats['total']:.2f}")
        print(f"  平均: {stats['average']:.2f}")
        print(f"  最大: {stats['max']:.2f}")
        print(f"  最小: {stats['min']:.2f}")
        print(f"  数量: {stats['count']}")
    
    return category_stats


# 示例5：自定义处理函数
@csv_parser('data/inventory.csv', delimiter=';')  # 支持不同的分隔符
def custom_processing(data: List[Dict[str, Any]], operation: str = 'summary') -> Any:
    """自定义数据处理"""
    print(f"执行自定义操作: {operation}")
    print("-" * 30)
    
    if operation == 'summary':
        # 生成数据摘要
        if data:
            print(f"数据字段: {list(data[0].keys())}")
            print(f"记录总数: {len(data)}")
            print(f"前3条记录:")
            for i, row in enumerate(data[:3]):
                print(f"  {i+1}: {row}")
    
    elif operation == 'validate':
        # 数据验证
        invalid_count = 0
        for i, row in enumerate(data):
            if not all(row.values()):  # 检查是否有空值
                invalid_count += 1
                print(f"第 {i+1} 行包含空值")
        print(f"\n共发现 {invalid_count} 条无效记录")
    
    else:
        print(f"未知操作: {operation}")
    
    return data


# 创建测试数据的函数
def create_test_data():
    """创建测试用的CSV文件"""
    os.makedirs('data', exist_ok=True)
    
    # 创建销售数据
    with open('data/sales.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'product', 'amount'])
        writer.writerows([
            ['2024-01-01', 'Product A', '1500.50'],
            ['2024-01-02', 'Product B', '2300.00'],
            ['2024-01-03', 'Product A', '1800.75'],
            ['2024-01-04', 'Product C', '950.25'],
            ['2024-01-05', 'Product B', '3200.00']
        ])
    
    # 创建学生数据
    with open('data/students.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'score', 'class'])
        writer.writerows([
            ['张三', '92.5', 'A'],
            ['李四', '78.0', 'B'],
            ['王五', '88.5', 'A'],
            ['赵六', '95.0', 'B'],
            ['钱七', '83.5', 'A']
        ])
    
    print("测试数据创建完成")


# 使用示例
if __name__ == "__main__":
    # 创建测试数据
    create_test_data()
    
    print("\n" + "="*60)
    print("示例1: 销售数据统计分析")
    print("="*60)
    result1 = analyze_sales_data()
    
    print("\n" + "="*60)
    print("示例2: 筛选优秀学生")
    print("="*60)
    result2 = filter_excellent_students(threshold=85.0)
    
    # 注释掉需要更多测试数据的示例
    # print("\n" + "="*60)
    # print("示例3: 导出JSON")
    # print("="*60)
    # export_to_json('products.json')
    
    # print("\n" + "="*60)
    # print("示例4: 按类别聚合")
    # print("="*60)
    # result4 = aggregate_by_category()
    
    # print("\n" + "="*60)
    # print("示例5: 自定义处理")
    # print("="*60)
    # custom_processing(operation='summary')
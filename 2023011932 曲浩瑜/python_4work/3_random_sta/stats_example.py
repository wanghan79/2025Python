"""
统计装饰器使用示例
"""

from data_generator import generate_data, stats_decorator
import json


def print_json(data):
    """以格式化的JSON打印数据"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


# 示例1：使用SUM和AVG统计学生成绩
print("示例1：使用SUM和AVG统计学生成绩")


@stats_decorator('SUM', 'AVG')
def generate_student_scores(count):
    return generate_data(
        length=count,
        student_id={"type": "sequence", "start": 10001},
        chinese={"type": "int", "min": 60, "max": 100},
        math={"type": "int", "min": 60, "max": 100},
        english={"type": "int", "min": 60, "max": 100},
        total_score={"type": "int", "min": 180, "max": 300}
    )


student_result = generate_student_scores(5)
print("学生数据:")
print_json(student_result['data'])
print("\n统计结果:")
print_json(student_result['stats'])
print("\n" + "-" * 50 + "\n")

# 示例2：使用MIN和MAX统计商品价格
print("示例2：使用MIN和MAX统计商品价格")


@stats_decorator('MIN', 'MAX')
def generate_products(count):
    return generate_data(
        length=count,
        product_id={"type": "sequence", "start": 1},
        name={"type": "string", "values": ["手机", "电脑", "平板", "手表", "耳机"]},
        price={"type": "float", "min": 99.9, "max": 9999.9, "precision": 2},
        stock={"type": "int", "min": 0, "max": 1000},
        discount_price={"type": "float", "min": 89.9, "max": 8999.9, "precision": 2}
    )


product_result = generate_products(10)
print("商品数据 (只显示前3条):")
print_json(product_result['data'][:3])
print("\n价格统计 (最高价和最低价):")
print_json(product_result['stats'])
print("\n" + "-" * 50 + "\n")

# 示例3：使用所有统计操作
print("示例3：使用所有统计操作 (SUM, AVG, MIN, MAX)")


@stats_decorator('SUM', 'AVG', 'MIN', 'MAX')
def generate_sales(count):
    return generate_data(
        length=count,
        order_id={"type": "uuid"},
        amount={"type": "float", "min": 100, "max": 10000, "precision": 2},
        quantity={"type": "int", "min": 1, "max": 20},
        discount={"type": "float", "min": 0, "max": 0.5, "precision": 2},
        status={"type": "string", "values": ["已完成", "已取消", "处理中"]}
    )


sales_result = generate_sales(20)
print("销售数据 (只显示前3条):")
print_json(sales_result['data'][:3])
print("\n销售统计:")
print_json(sales_result['stats'])

# 示例4：对嵌套数据结构进行统计
print("\n示例4：对嵌套数据结构进行统计")


@stats_decorator('SUM', 'AVG')
def generate_department_stats(count):
    # 将生成器结果转换为列表，避免生成器被消耗的问题
    dept_data = list(generate_data(
        length=count,
        dept_id={"type": "sequence", "start": 1},
        name={"type": "string", "values": ["研发部", "市场部", "销售部", "财务部", "人力资源部"]},
        budget={"type": "float", "min": 10000, "max": 1000000, "precision": 2},
        staff_count={"type": "int", "min": 5, "max": 200}
    ))

    # 手动计算人均预算
    for dept in dept_data:
        if 'budget' in dept and 'staff_count' in dept and dept['staff_count'] > 0:
            dept['budget_per_person'] = round(dept['budget'] / dept['staff_count'], 2)

    return dept_data


dept_result = generate_department_stats(5)
print("部门数据:")
print_json(dept_result['data'])
print("\n部门预算统计:")
print_json(dept_result['stats'])

if __name__ == "__main__":
    print("\n带参数装饰器可以灵活组合SUM、AVG、MAX、MIN等统计操作")

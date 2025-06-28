from data_generator import generate_data
import json


def print_json(data):
    print(json.dumps(list(data), ensure_ascii=False, indent=2))


print("示例1：生成简单用户数据")
users = generate_data(
    length=3,
    id={"type": "sequence", "start": 1001},
    username={"type": "string", "length": 8},
    is_active={"type": "bool", "weight": 0.8}
)
print_json(users)
print("\n" + "-" * 50 + "\n")

print("示例2：生成产品数据")
products = generate_data(
    length=2,
    id={"type": "uuid"},
    name={"type": "string", "values": ["智能手机", "笔记本电脑", "平板电脑", "智能手表", "无线耳机"]},
    price={"type": "float", "min": 1000, "max": 10000, "precision": 2},
    stock={"type": "int", "min": 0, "max": 1000},
    created_at={"type": "datetime", "start": "2023-01-01", "end": "2023-12-31"}
)
print_json(products)
print("\n" + "-" * 50 + "\n")

print("示例3：生成嵌套结构的订单数据")
orders = generate_data(
    length=2,
    order_id={"type": "uuid"},
    customer={
        "type"  : "dict",
        "schema": {
            "id"   : {"type": "sequence", "start": 2001},
            "name" : {"type": "string", "charset": "chinese", "length": 3},
            "email": {"type": "string", "length": 10}
        }
    },
    items={
        "type"      : "list",
        "of"        : {
            "type"  : "dict",
            "schema": {
                "product_id": {"type": "sequence", "start": 100},
                "name"      : {"type": "string", "values": ["手机壳", "充电器", "数据线", "耳机", "钢化膜"]},
                "price"     : {"type": "float", "min": 10, "max": 200, "precision": 2},
                "quantity"  : {"type": "int", "min": 1, "max": 5}
            }
        },
        "min_length": 1,
        "max_length": 3
    },
    total_amount={"type": "float", "min": 100, "max": 5000, "precision": 2},
    status={"type": "string", "values": ["待付款", "已付款", "已发货", "已完成", "已取消"]},
    created_at={"type": "datetime"}
)
print_json(orders)
print("\n" + "-" * 50 + "\n")

print("示例4：生成学生成绩数据")
student_grades = generate_data(
    length=3,
    student_id={"type": "sequence", "start": 20210001},
    name={"type": "string", "charset": "chinese", "length": 3},
    class_id={"type": "string", "values": ["一年级(1)班", "一年级(2)班", "二年级(1)班"]},
    scores={
        "type"  : "dict",
        "schema": {
            "语文": {"type": "int", "min": 60, "max": 100},
            "数学": {"type": "int", "min": 60, "max": 100},
            "英语": {"type": "int", "min": 60, "max": 100},
            "科学": {"type": "int", "min": 60, "max": 100}
        }
    },
    attendance={"type": "float", "min": 0.8, "max": 1.0, "precision": 2},
    comments={"type": "string", "charset": "chinese", "length": 20}
)
print_json(student_grades)

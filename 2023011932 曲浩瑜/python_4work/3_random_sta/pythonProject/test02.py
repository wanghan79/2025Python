from test1 import generate_data, get_statistics, clear_statistics
import json


def print_json(data):
    print(json.dumps(list(data), ensure_ascii=False, indent=2))


def generate_and_show_stats(example_name, config):
    print(f"\n{example_name}")
    clear_statistics()

    data = generate_data(**config)
    data_list = list(data)
    print_json(data_list)

    stats = get_statistics()
    if stats:
        print("\n统计信息:")
        for field, metrics in stats.items():
            print(f"  {field}:")
            for metric, value in metrics.items():
                print(f"    {metric}: {value}")
    else:
        print("\n(没有可用的数值类型统计信息)")

    print("\n" + "-" * 50 + "\n")
    return data_list


# 示例1：生成简单用户数据
generate_and_show_stats(
    "测试统计功能",
    {
        "length": 5,
        "score": {"type": "int", "min": 60, "max": 100},  # 会被统计
        "price": {"type": "float", "min": 10.5, "max": 20.5, "precision": 2}  # 会被统计
    }
)
import csv
import statistics as st
from collections import defaultdict
from functools import wraps
from pathlib import Path
from typing import List, Dict, Any, Callable, Tuple

def csv_loader(path: str, encoding: str = "utf-8") -> Callable:

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            rows: List[Dict[str, Any]] = []
            with open(path, newline="", encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)

            # 自动识别数值列
            numeric_cols, cat_cols = _split_columns(rows)

            # 缺失值 / 类型转换
            _clean_rows(rows, numeric_cols)

            meta = {
                "numeric_cols": numeric_cols,
                "categorical_cols": cat_cols,
                "path": path,
            }
            return func(rows, meta, *args, **kwargs)

        return wrapper
    return decorator

def _split_columns(rows: List[Dict[str, str]]) -> Tuple[List[str], List[str]]:
    numeric_cols, cat_cols = [], []
    sample = rows[0]
    for col, val in sample.items():
        try:
            float(val)
            numeric_cols.append(col)
        except ValueError:
            cat_cols.append(col)
    return numeric_cols, cat_cols

def _clean_rows(rows: List[Dict[str, str]], num_cols: List[str]) -> None:
    for row in rows:
        for c in list(row):
            if c in num_cols:
                row[c] = float(row[c]) if row[c] else 0.0
            else:
                row[c] = row[c] or "NA"

@csv_loader("students.csv")
def full_report(data: List[Dict[str, Any]], meta: Dict[str, Any]) -> None:
    numeric = [c for c in meta["numeric_cols"] if c not in ("age", "absent_days")]
    cat = meta["categorical_cols"]
    print(f"\n文件：{meta['path']}")
    print(f"数值列: {numeric}")
    print(f"类别列: {cat}\n")

    # 2.1 各科描述统计
    print("=== 科目均值 / 方差 / 最高分 ===")
    for col in numeric:
        scores = [row[col] for row in data]
        mean, var, top = st.mean(scores), st.pvariance(scores), max(scores)
        print(f"{col:<10} 平均 {mean:6.2f}  方差 {var:7.2f}  最高 {top:5.1f}")

    # 2.2 每位同学 GPA & 总分
    for row in data:
        row["total"] = sum(row[c] for c in numeric)
        row["gpa"] = calc_gpa(row["total"] / len(numeric))

    # 2.3 按班级统计平均 GPA
    classes = defaultdict(list)
    for row in data:
        classes[row["class"]].append(row["gpa"])

    print("\n=== 各班平均 GPA ===")
    for cls, gpas in classes.items():
        print(f"class {cls:<5} → {st.mean(gpas):.2f}")

    # 2.4 Top 10
    data.sort(key=lambda r: r["total"], reverse=True)
    top10 = data[:10]
    print("\n=== Top 10 by Total Score ===")
    for i, r in enumerate(top10, 1):
        print(f"{i:02d}. {r['name']:<10} {r['total']:.1f}  GPA {r['gpa']:.2f}")

def calc_gpa(score: float) -> float:

    return round((score / 100) * 4, 2)

def write_csv(path: str, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    full_report()
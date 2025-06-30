from typing import Dict, Optional
from largeXMLDealer import xml_parser_decorator

# 应用修饰器配置
@xml_parser_decorator(
    file_path="large_data.xml",
    target_elements=["employee", "department", "salary"]
)
def print_business_report(
    company_data: Dict[str, Any],
    xml_stats: Optional[Dict[str, List[str]]] = None
):
    """
    业务数据报告打印函数
    :param company_data: 公司业务数据字典
    :param xml_stats: 从修饰器注入的XML统计数据
    """
    print("\n=== 公司业务报告 ===")
    print(f"公司名称: {company_data.get('name', '未知')}")
    print(f"报告周期: {company_data.get('period', '2023年度')}")
    
    if xml_stats:
        print("\n[员工数据分析]")
        print(f"总员工数: {len(xml_stats['employee'])}")
        print(f"部门分布: {', '.join(set(xml_stats['department']))}")
        
        if 'salary' in xml_stats:
            salaries = [int(s) for s in xml_stats['salary'] if s.isdigit()]
            if salaries:
                print(f"平均薪资: {sum(salaries)/len(salaries):.2f}元")
    else:
        print("\n[警告] 无有效的员工数据")

if __name__ == "__main__":
    # 测试数据
    test_data = {
        "name": "ABC科技有限公司",
        "period": "2023年Q2",
        "revenue": "1.2亿"
    }
    
    # 调用被装饰的函数
    print_business_report(test_data)

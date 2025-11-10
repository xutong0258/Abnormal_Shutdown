from bs4 import BeautifulSoup
import csv
from base.logger import *

def parse_html_table(html_file):
    # 读取HTML文件内容
    # with open(html_file, 'r', encoding='utf-8') as f:
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'latin1']
    html_content = None
    for enc in encodings:
        try:
            with open(html_file, 'r', encoding=enc) as f:
                html_content = f.read()
            break  # Success
        except UnicodeDecodeError:
            continue
    if html_content is None:
        raise ValueError(f"Unable to decode file: {html_file}")
    
    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有 table 标签
    tables = soup.find_all('table')

    print(f"共找到 {len(tables)} 个表格")

    # 遍历每个表格（可选：打印或进一步处理）
    for i, table in enumerate(tables, 1):
        print(f"\n=== 表格 {i} ===")
        # 可选：将表格转为文本或提取数据
        print(table.prettify())  # 美化输出 HTML
    
    return

def save_to_csv(headers, rows, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"数据已保存到 {output_file}")

if __name__ == "__main__":
    # 解析HTML文件
    parse_html_table('SystemPowerReport.html')
    
    # # 打印解析结果（前5行）
    # if headers and rows:
    #     print("表头：")
    #     print(headers)
    #     print("\n前5行数据：")
    #     # for i, row in enumerate(rows[:5]):
    #     #     print(f"行 {i+1}: {row}")
    #
    #     # 保存为CSV文件
    #     save_to_csv(headers, rows, 'power_report.csv')

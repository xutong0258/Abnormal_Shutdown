from bs4 import BeautifulSoup
import csv
from base.logger import *

def parse_html_table(html_file):
    # 读取HTML文件内容
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
    
    # 找到目标表格（id为summary-table的表格）
    table = soup.find('table', id='summary-table')
    # logger.info(f'table:{table}')
    if not table:
        print("未找到目标表格")
        return
    
    # 提取表头
    headers = []
    thead = table.find('thead')
    if thead:
        th_tags = thead.find_all('th')
        headers = [th.get_text(strip=True) for th in th_tags]
        # logger.info(f'headers:{headers}')
    
    # 提取表格内容
    rows = []
    tbody = table.find('tbody')
    if tbody:
        tr_tags = tbody.find_all('tr')
        for tr in tr_tags:
            td_tags = tr.find_all('td')
            # 处理每个单元格内容，替换<br>为换行符
            row_data = []
            for td in td_tags:
                # 将<br>标签替换为换行符
                for br in td.find_all('br'):
                    br.replace_with('\n')
                row_data.append(td.get_text(strip=False).strip())
            rows.append(row_data)
    
    return headers, rows

def save_to_csv(headers, rows, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"数据已保存到 {output_file}")

if __name__ == "__main__":
    # 解析HTML文件
    headers, rows = parse_power_report('KernelPowerReport.html')
    
    # 打印解析结果（前5行）
    if headers and rows:
        print("表头：")
        print(headers)
        print("\n前5行数据：")
        # for i, row in enumerate(rows[:5]):
        #     print(f"行 {i+1}: {row}")
        
        # 保存为CSV文件
        save_to_csv(headers, rows, 'power_report.csv')

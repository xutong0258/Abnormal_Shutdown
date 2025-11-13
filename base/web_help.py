from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def parse_dynamic_table(html_path):
    # 初始化浏览器驱动（使用Chrome为例）
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # 加载本地HTML文件（如果是在线网页，替换为URL即可）
        driver.get(f"file:///{html_path}")
        
        # 等待页面关键元素加载完成（根据网页中的表格ID调整）
        # 示例：等待summary-table表格加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "summary-table"))
        )
        
        # 存储所有表格数据的列表
        all_tables = []
        
        # 获取页面中所有表格（可根据需要筛选特定表格）
        tables = driver.find_elements(By.TAG_NAME, "table")
        
        for table in tables:
            # 提取表格ID（用于标识表格）
            table_id = table.get_attribute("id") or f"table_{len(all_tables)}"
            
            # 提取表头
            headers = []
            th_elements = table.find_elements(By.TAG_NAME, "th")
            for th in th_elements:
                headers.append(th.text.strip())
            
            # 提取表格内容
            rows = []
            tr_elements = table.find_elements(By.TAG_NAME, "tr")
            for tr in tr_elements[1:]:  # 跳过表头行
                tds = tr.find_elements(By.TAG_NAME, "td")
                row = [td.text.strip() for td in tds]
                if row:  # 跳过空行
                    rows.append(row)
            
            # 存储表格数据（ID、表头、内容）
            all_tables.append({
                "table_id": table_id,
                "headers": headers,
                "data": rows
            })
        
        return all_tables
    
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    # 替换为你的HTML文件路径
    html_file_path = r"D:\SystemPowerReport.html"  # 例如：C:/reports/SystemPowerReport.html
    
    # 解析表格
    tables_data = parse_dynamic_table(html_file_path)
    
    # 打印结果（或保存为CSV/Excel）
    for table in tables_data:
        print(f"表格ID: {table['table_id']}")
        print("表头:", table['headers'])
        print("内容行数:", len(table['data']))
        print(table['data'])
        # print("示例数据:", table['data'][0] if table['data'] else "无数据")
        # print("-" * 50)
    
    # # 可选：将第一个表格转换为DataFrame并保存为CSV
    # if tables_data:
    #     first_table = tables_data[0]
    #     df = pd.DataFrame(first_table['data'], columns=first_table['headers'])
    #     df.to_csv("parsed_table.csv", index=False, encoding="utf-8")
    #     print("已保存第一个表格到 parsed_table.csv")

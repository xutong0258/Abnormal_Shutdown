from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import csv
from base.logger import *
from base.folder_file import *

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

def parse_dynamic_table(html_path):
    logger.info(f'parse_dynamic_table')
    # 初始化浏览器驱动（使用Chrome为例）
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Firefox()
    logger.info(f'driver')
    try:
        # 加载本地HTML文件（如果是在线网页，替换为URL即可）
        driver.get(f"file:///{html_path}")
        
        # 等待页面关键元素加载完成（根据网页中的表格ID调整）
        # 示例：等待summary-table表格加载
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "summary-table"))
        )
        logger.info(f'WebDriverWait end')
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
            # logger.info(f'th_elements:{th_elements}')
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

def get_Abnormal_Shutdown_time(folder_path):
    # logger.info(f'target_list:{target_list}')
    # logger.info(f'row:{row}')

    target_file = 'SystemPowerReport.html'
    file_path = get_file_path_by_dir(folder_path, target_file)
    logger.info(f'file_path:{file_path}')

    # 解析表格
    tables_data = parse_dynamic_table(file_path)

    # 打印结果（或保存为CSV/Excel）
    target_str = 'START TIME'
    target_table = None
    target_time = None
    for table in tables_data:
        if target_str in table['headers'] and 'Abnormal Shutdown' in table['data'][0]:
            target_elem =table['data'][0]
            target_time = target_elem[1]
            logger.info(f'target_elem:{target_elem}')
            logger.info(f'target_time:{target_time}')

    return target_time

def Critical_Event_Check(folder_path):
    # logger.info(f'target_list:{target_list}')
    # logger.info(f'row:{row}')

    target_file = 'KernelPowerReport.html'
    file_path = get_file_path_by_dir(folder_path, target_file)
    logger.info(f'file_path:{file_path}')

    # 解析表格
    tables_data = parse_dynamic_table(file_path)

    # 打印结果（或保存为CSV/Excel）
    target_str = 'TimeCreated'
    target_table = None
    target_time = None
    match_check = False
    for table in tables_data:
        if target_str in table['headers'] and 'Critical' in table['data'][0] and '41' in table['data'][0]:
            target_list =table['data'][0]
            logger.info(f'target_list:{target_list}')
            for item in target_list:
                if 'BugcheckCode:0x0' in item:
                    match_check = True
                    break

    logger.info(f'match_check:{match_check}')
    return match_check

def get_wakeup_reason(folder_path):
    # logger.info(f'target_list:{target_list}')
    # logger.info(f'row:{row}')

    target_file = 'KernelPowerReport.html'
    file_path = get_file_path_by_dir(folder_path, target_file)
    logger.info(f'file_path:{file_path}')

    # 解析表格
    tables_data = parse_dynamic_table(file_path)

    target_str = 'TimeCreated'
    target_table = None
    target_time = None
    wakeup_reason = None
    for table in tables_data:
        # logger.info(f'table:{table}')
        if target_str in table['headers']:
            target_list = table['data']
            for item in target_list:
                # logger.info(f'item:{item}')
                if '1' in item[1] and '唤醒源' in item[4]:
                    wakeup_reason = item[4]
                    match = re.search(r'唤醒源:(.*)\n', wakeup_reason)
                    if match:
                        wakeup_reason = match.group()
                        # wakeup_reason = wakeup_reason.replace('唤醒源:', '')
                    else:
                        logger.info("未找到wakeup_reason")
                    break
    logger.info(f'wakeup_reason:{wakeup_reason}')
    return wakeup_reason
if __name__ == "__main__":
    folder_path = r'D:\00\04_异常关机重启唤不醒\睡眠休眠异常_log\S3 abnoamal resume'
    wakeup_reason = get_wakeup_reason(folder_path)
    # logger.info(f'wakeup_reason:{wakeup_reason}')


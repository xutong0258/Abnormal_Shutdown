from bs4 import BeautifulSoup
from selenium import webdriver

# 启动浏览器（需下载对应浏览器驱动，如ChromeDriver）
driver = webdriver.Chrome()
html_file = r"D:\SystemPowerReport.html"  # Windows（使用原始字符串）

driver.get(html_file)  # 本地文件路径
# html_content = driver.page_source  # 获取动态加载后的HTML
# driver.quit()
#
# # 后续解析逻辑同上（用html_content创建soup）
#
# # 读取HTML文件内容
# with open("SystemPowerReport.html", "r", encoding="utf-8") as f:
#     html_content = f.read()

# 解析HTML
soup = BeautifulSoup(html_content, "html.parser")

# 定位"Filter Option"下方的表格（根据实际HTML结构调整选择器）
# 假设表格前有包含"Filter Option"的标题，通过标题定位相邻表格
filter_option_label = soup.find(string=lambda text: text and "Filter Option" in text)
if filter_option_label:
    # 获取标题的父元素，再查找后续的表格
    filter_table = filter_option_label.find_parent().find_next("table")
    print(f'{filter_table}')

    if filter_table:
        # 提取表头
        headers = []
        for th in filter_table.find_all("th"):
            headers.append(th.get_text(strip=True))

        # 提取表格内容
        rows = []
        for tr in filter_table.find_all("tr")[1:]:  # 跳过表头行
            row = [td.get_text(strip=True) for td in tr.find_all("td")]
            rows.append(row)

        # 打印结果
        print("表头:", headers)
        print("表格内容:")
        for row in rows:
            print(row)
    else:
        print("未找到Filter Option对应的表格")
else:
    print("未找到包含'Filter Option'的标签")

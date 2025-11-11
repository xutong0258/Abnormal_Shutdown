import os
from base.logger import *
from base.fileOP import *
from base.helper import *
from base.html_parse import *
from base.svctx_parse import *

def shutdown_check_rule_2(folder_path):
    logger.info(f'folder_path:{folder_path}')

    target_file = 'KernelPowerReport.html'
    file_path = get_file_path_by_dir(folder_path, target_file)

    # 解析HTML文件
    headers, rows = parse_html_table(file_path)
    target_list = ['41', 'Critical', 'BugcheckCode:0x0']
    match_check = False
    for row in rows:
        match_check = is_target_list_in_row(target_list, row)
        if match_check == True:
            break
    logger.info(f'match_check:{match_check}')
    return match_check

def shutdown_check_rule_3(folder_path):
    logger.info(f'folder_path:{folder_path}')

    target_file = '.evtx'
    evtx_path = get_file_path_by_dir(folder_path, target_file)
    # evtx_path = r"D:\System.evtx"
    match_id = False
    match_Provider = False
    match_case_3 = False
    with Evtx(evtx_path) as log:
        for i, record in enumerate(log.records()):
            if i >= 10:  # 仅显示前10条
                pass
            try:
                parsed = parse_event_record(record.xml())
                # print(f"Time: {parsed['TimeCreated']}")
                # print(f"EventID: {parsed['EventID']}")
                # print(f"Level: {parsed['Level']}")
                # print(f"Provider: {parsed['Provider']}")
                # print("-" * 50)
                if '41' in parsed['EventID']:
                    match_id = True
                if 'BugcheckCode:0x0' in parsed['Provider']:
                    match_Provider = True
                if match_id and match_Provider:
                    match_case_3 = True
                    break

            except Exception as e:
                print(f"解析错误: {e}")

    logger.info(f'match_case_3:{match_case_3}')
    return match_case_3

def shutdown_check_rule_4(folder_path):
    logger.info(f'folder_path:{folder_path}')
    return_dict = None
    out_dict_ec = {'rule_name': 'shutdown_check_rule_4',
                'Exception': '此次关机事件是由EC这边拉电执行的',
                'Debug Solution': ''}

    out_dict = {'rule_name': 'shutdown_check_rule_4',
                'Exception': '此关机/重启不是EC这边拉电导致的',
                'Debug Solution': ''}

    target_file = 'ShutDownID(LBG).txt'
    target_file = get_file_path_by_dir(folder_path, target_file)

    log_line = get_file_content_list(target_file)
    target_str = '0x01'
    count = get_list_text_count(log_line, target_str)
    if count == 0:
        return_dict = out_dict_ec
    else:
        return_dict = out_dict

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def wakeup_check_rule_1(folder_path):
    logger.info(f'folder_path:{folder_path}')

    target_file = 'KernelPowerReport.html'
    file_path = get_file_path_by_dir(folder_path, target_file)

    # 解析HTML文件
    headers, rows = parse_html_table(file_path)
    target_list = ['41', 'Critical', 'BugcheckCode:0x0']
    match_check = False
    check_result = ''
    for row in rows:
        if '1' == row[1]:
            check_result = row[4]
            break
    logger.info(f'check_result:{check_result}')
    return
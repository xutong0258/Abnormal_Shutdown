import os
from base.logger import *
from base.fileOP import *
from base.helper import *
from base.web_help import *
from base.svctx_parse import *

def shutdown_check_rule_1(folder_path):
    logger.info(f'folder_path:{folder_path}')

    # folder_path = r'D:\hello'
    target_time = get_Abnormal_Shutdown_time(folder_path)
    return target_time

def shutdown_check_rule_2(folder_path):
    logger.info(f'folder_path:{folder_path}')

    match_check = Critical_Event_Check(folder_path)
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

def check_ShutdownID_01(folder_path):
    is_ShutdownID_01 = False
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
        is_ShutdownID_01 = False
    else:
        return_dict = out_dict
        is_ShutdownID_01 = True

    logger.info(f'return_dict:{return_dict}')
    return is_ShutdownID_01

def check_is_abnormal_shutdown(folder_path):
    is_abnormal_shutdown = False

    check_flag_1 = False
    target_time = shutdown_check_rule_1(folder_path)
    logger.info(f'target_time:{target_time}')
    if target_time is not None:
        check_flag_1 = True

    check_flag_2 = False
    match_check = shutdown_check_rule_2(folder_path)
    logger.info(f'match_check:{match_check}')
    if match_check == True:
        check_flag_2 = True

    check_flag_3 = False
    match_check = shutdown_check_rule_3(folder_path)
    logger.info(f'match_check:{match_check}')
    if match_check == True:
        check_flag_3 = True

    if check_flag_1 and check_flag_2 and check_flag_3:
        is_abnormal_shutdown = True
    return is_abnormal_shutdown

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
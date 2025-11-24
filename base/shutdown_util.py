import os
from base.contants import *
from utils.logger_util import *
from base.fileOP import *
from base.web_help import *
from base.svctx_parse import *
from base.translator_help import *

path_dir = os.path.dirname(__file__)

table_file = 'table.yaml'
table_file = os.path.join(CONFIG_PATH, table_file)

if os.path.exists(table_file):
    table_dict = read_file_dict(table_file)

def get_list_text_line(input_list, text):
    text = text.lower()
    text_line = None
    for item in input_list:
        item = item.lower()
        # logger.info(f'item:{item}')
        if text in item:
            text_line = item.strip()
    return text_line

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
            try:
                parsed = parse_event_record(record.xml())
                # print(f"Time: {parsed['TimeCreated']}")
                # print(f"EventID: {parsed['EventID']}")
                # print(f"Level: {parsed['Level']}")
                # print(f"Provider: {parsed['Provider']}")
                # print("-" * 50)
                # logger.info(f'parsed:{parsed}')
                if '41' in parsed['EventID']:
                    match_id = True
                    logger.info(f'parsed:{parsed}')
                if 'BugcheckCode:0x0' in parsed['Provider']:
                    match_Provider = True
                if match_id and match_Provider:
                    match_case_3 = True
                    break

            except Exception as e:
                print(f"解析错误: {e}")
    if match_case_3 == False:
        logger.info(f'evtx hasn\'t BugcheckCode:0x0 record')
    logger.info(f'match_case_3:{match_case_3}')
    return match_case_3

def check_ShutdownID(folder_path, log_path):
    logger.info(f'folder_path:{folder_path}')
    target_file = 'ShutDownID(LBG).txt'
    target_file = get_file_path_by_dir(folder_path, target_file)

    if target_file is None:
        return

    log_lines = get_file_content_list(target_file)
    target_str = 'The last 1st:'
    text_line = get_list_text_line(log_lines, target_str)
    logger.info(f'text_line:{text_line}')

    ShutdownID = text_line.replace('the last 1st:', '')
    tmp_list = ShutdownID.split('(')
    ShutdownID = tmp_list[0].strip()
    logger.info(f'ShutdownID:{ShutdownID}')

    # ShutdownID = '04'
    if '0X' not in ShutdownID:
        ShutdownID = f'0x{ShutdownID}'

    result_dic = table_dict.get(ShutdownID, None)
    result_dic['ShutdownID'] = ShutdownID

    logger.info(f'result_dic:{result_dic}')
    return result_dic

def check_is_abnormal_shutdown(folder_path):
    is_abnormal_shutdown = False

    check_flag_1 = False
    target_time = shutdown_check_rule_1(folder_path)
    logger.info(f'target_time:{target_time}')
    if target_time is None:
        return is_abnormal_shutdown

    if target_time is not None:
        check_flag_1 = True

    check_flag_2 = False
    match_check = shutdown_check_rule_2(folder_path)
    logger.info(f'match_check:{match_check}')
    if match_check == False:
        return is_abnormal_shutdown

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

def parese_shutdown_cfg_to_dict():
    file = 'Shutdown_ID.txt'
    file = os.path.join(CONFIG_PATH, file)
    log_lines = get_file_content_list(file)
    # logger.info(f'log_lines:{log_lines}')
    total_dict = dict()
    for log_line in log_lines:
        log_line = log_line.strip()
        if not log_line.startswith('//') and len(log_line) > 0:
            cell_dict = {}
            # logger.info(f'log_line:{log_line}')
            tmp_list = log_line.split('//')
            # logger.info(f'tmp_list:{tmp_list}')
            shutdown_id = tmp_list[0]

            root_casue = ''
            root_casue_ch = ''
            if len(tmp_list) >= 2:
                root_casue = tmp_list[1].strip()
                root_casue_ch = get_translator_zh_CN(root_casue)

            match = re.search(r'0x(.*)\t', shutdown_id)

            if match:
                shutdown_id = match.group()
                # logger.info(f'shutdown_id:{shutdown_id}')
            else:
                match = re.search(r'0x(.*) ', shutdown_id)
            shutdown_id = shutdown_id.strip()
            shutdown_id = shutdown_id.replace(' ', '\t')
            shutdown_id = shutdown_id.split('\t')[-1]

            logger.info(f'shutdown_id:{shutdown_id}')
            cell_dict = {'root_casue': root_casue, '原因': root_casue_ch}
            total_dict[shutdown_id] = cell_dict

    file_name = 'table.yaml'
    file_name = os.path.join(CONFIG_PATH, file_name)

    dump_file(file_name, total_dict)
    return
if __name__ == '__main__':
    parese_shutdown_cfg_to_dict()
    pass
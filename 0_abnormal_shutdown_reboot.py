import os
from base import fileOP
from base.common import *
from base.shutdown_util import *

path_dir = os.path.dirname(__file__)
logger.info(f'path_dir: {path_dir}')

def copy_files(result_dir):
    files = ['tmp.log',
             'BSOD_Debug_Data.yaml',
             'BSOD_Debug_Report.yaml',
             'result.yaml',
             'step_command.yaml',
             'command_dict.yaml',
             ]
    src_files = []
    for item in files:
        file = os.path.join(path_dir, item)
        src_files.append(file)
    copy_multiple_files(src_files, result_dir)
    return

file = r'D:\input.yaml'
src_dir_list = fileOP.get_file_content_list(file)
# logger.info(f'src_dir_list: {src_dir_list}')

src_dir_list = [r'G:\BSOD_Debug_SOP_0911\1. Automatic\1.1 0x3b_Context Memory Corruption',
                ]

if __name__ == '__main__':
    folder_path = r'D:\00\04_异常关机重启唤不醒\log\ALADDIN'
    folder_path = r'D:\00\04_异常关机重启唤不醒\异常关机重启_log\OneDrive_8_2025-10-30\JINGWEI2_IML-SVT-LE46081L004-41A6B8AB\ThinkPad E14 Gen 6_PF5XNHNZ_2025_10_20_08_04_12'
    is_abnormal_shutdown = check_is_abnormal_shutdown(folder_path)
    logger.info(f'is_abnormal_shutdown:{is_abnormal_shutdown}')

    is_ShutdownID_01 = False
    if is_abnormal_shutdown:
        is_ShutdownID_01 = check_ShutdownID_01(folder_path)

    logger.info(f'is_ShutdownID_01:{is_ShutdownID_01}')
    # diction output
    if is_abnormal_shutdown == True and is_ShutdownID_01 == False:
        logger.info(f'diction output')
    pass
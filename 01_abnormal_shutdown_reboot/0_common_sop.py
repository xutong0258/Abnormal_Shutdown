import os
import sys

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)

root_dir = os.path.join(path_dir, '../')
sys.path.append(root_dir)

from utils.logger_util import logger
from base.fileOP import dump_file, add_string_to_first_line
from base.shutdown_util import check_is_abnormal_shutdown, check_ShutdownID

path_dir = os.path.dirname(__file__)
logger.info(f'path_dir: {path_dir}')


if __name__ == '__main__':
    folder_path = r'test_data\01_异常关机重启_log\ALADDIN'
    folder_path = os.path.join(path_dir, '../', folder_path)
    folder_path = r'D:\02_异常重启\YOGA 360 14 IPH11X_PF5TS0SD_2025_11_24_13_44_41'
    # logger.info(f'folder_path: {folder_path}')

    is_abnormal_shutdown,result_dic = check_is_abnormal_shutdown(folder_path, path_dir)
    logger.info(f'is_abnormal_shutdown:{is_abnormal_shutdown}')

    file_name = '异常关机重启_result.yaml'
    file_name = os.path.join(path_dir, file_name)

    if result_dic is not None:
        dump_file(file_name, result_dic)

    # if is_abnormal_shutdown == True:
    tmp_dic = check_ShutdownID(folder_path, path_dir)

    if tmp_dic is not None:
        result_dic['ShutdownID'] = tmp_dic
        dump_file(file_name, result_dic)

    prefix_text = f'异常关机/重启: {is_abnormal_shutdown}'
    add_string_to_first_line(file_name, prefix_text)
    pass
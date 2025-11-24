import os
import sys

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)

root_dir = os.path.join(path_dir, '../')
sys.path.append(root_dir)

from base.shutdown_util import *

path_dir = os.path.dirname(__file__)
logger.info(f'path_dir: {path_dir}')


if __name__ == '__main__':
    folder_path = r'test_data\01_异常关机重启_log\ALADDIN'
    folder_path = os.path.join(path_dir, '../', folder_path)
    folder_path = r'D:\00\04_异常关机重启唤不醒\01_异常关机重启_log\ALADDIN'
    logger.info(f'folder_path: {folder_path}')

    is_abnormal_shutdown = check_is_abnormal_shutdown(folder_path)
    logger.info(f'is_abnormal_shutdown:{is_abnormal_shutdown}')

    # if is_abnormal_shutdown == True:
    result_dic = check_ShutdownID(folder_path, path_dir)

    if result_dic is not None:
        file_name = '异常关机重启_result.yaml'
        file_name = os.path.join(path_dir, file_name)

        dump_file(file_name, result_dic)
    pass
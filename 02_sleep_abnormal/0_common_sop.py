import os
import sys

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)

root_dir = os.path.join(path_dir, '../')
sys.path.append(root_dir)

from base.shutdown_util import *
from base.fileOP import dump_file

path_dir = os.path.dirname(__file__)
logger.info(f'path_dir: {path_dir}')

if __name__ == '__main__':
    folder_path = r'D:\异常关机、异常重启和睡眠休眠异常\03_睡眠休眠异常\S3_Resume_abnormal'
    # folder_path = os.path.join(path_dir, '../', folder_path)
    logger.info(f'folder_path: {folder_path}')
    # 唤醒源
    result_dict, latest_reason = get_wakeup_reason(folder_path)
    logger.info(f'latest_reason:{latest_reason}')

    file_name = '唤不醒_result.yaml'
    file_name = os.path.join(path_dir, file_name)

    dump_file(file_name, result_dict)
    pass
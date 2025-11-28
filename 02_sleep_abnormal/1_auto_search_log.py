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
    case_path_config_file = 'case_path_config.yaml'
    case_path_config_file = os.path.join(CONFIG_PATH, case_path_config_file)
    table_dict = read_file_dict(case_path_config_file)
    case_dict = table_dict.get('04_异常唤不醒')

    folder_path = case_dict.get('PATH')
    logger.info(f'folder_path: {folder_path}')

    # 唤醒源
    result_dict, latest_reason = get_wakeup_reason(folder_path)
    logger.info(f'latest_reason:{latest_reason}')

    file_name = '唤不醒_result.yaml'
    file_name = os.path.join(path_dir, file_name)

    dump_file(file_name, result_dict)
    pass
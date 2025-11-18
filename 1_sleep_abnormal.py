import os
from base import fileOP
from base.common import *
from base.shutdown_util import *

path_dir = os.path.dirname(__file__)
logger.info(f'path_dir: {path_dir}')

if __name__ == '__main__':
    folder_path = r'D:\00\04_异常关机重启唤不醒\睡眠休眠异常_log\S3 abnoamal resume'
    wakeup_reason = get_wakeup_reason(folder_path)
    pass
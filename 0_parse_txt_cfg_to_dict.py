import os
import sys

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)

root_dir = os.path.join(path_dir, '../')
sys.path.append(root_dir)

from base.shutdown_util import *

if __name__ == '__main__':
    parese_shutdown_cfg_to_dict()
    pass

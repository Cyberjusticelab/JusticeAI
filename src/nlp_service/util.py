import os
import sys

def load_src_dir_to_sys_path():
    parent_dir = os.getcwd() + "/.."
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)


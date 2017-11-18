import os
from enum import Enum

class Path:
    """
    Super annoying relative imports done here
    """
    root_directory = os.path.abspath(__file__ + "r/../")

    __rel_path = r'data/raw/'
    raw_data_directory = os.path.join(root_directory, __rel_path)

    __rel_path = r'data/binary/'
    binary_directory = os.path.join(root_directory, __rel_path)

    __rel_path = r'data/cache/'
    cache_directory = os.path.join(root_directory, __rel_path)
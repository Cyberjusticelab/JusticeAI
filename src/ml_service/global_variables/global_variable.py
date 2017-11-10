import os
from enum import Enum


class InformationType(Enum):
    FACTS = 1
    PRECEDENTS_FILE_NAMES = 2
    PROCESSED_FACTS = 3


class Global:
    """
    Change these variables to make code work on your machine
    tmp solution since we can't download models online via
    HTTP
    """

    __script_dir = os.path.abspath(__file__ + "/../../")
    __rel_path = r'precedents/text_bk/'
    Precedence_Directory = os.path.join(__script_dir, __rel_path)

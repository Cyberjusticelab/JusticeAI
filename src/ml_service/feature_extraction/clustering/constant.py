import os
from enum import Enum


class InformationType(Enum):
    FACTS = 1
    PRECEDENTS_FILE_NAMES = 2
    PROCESSED_FACTS = 3
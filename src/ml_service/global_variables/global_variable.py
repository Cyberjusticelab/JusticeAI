import os
from enum import Enum


class InformationType(Enum):
    FACTS = 1
    PRECEDENTS_FILE_NAMES = 2
    PROCESSED_FACTS = 3


class Global:
    """
    Super annoying relative imports done here
    """

    __script_dir = os.path.abspath(__file__ + "/../../")
    __rel_path = r'precedents/text_bk/'
    precedent_directory = os.path.join(__script_dir, __rel_path)

    __rel_path = r'ml_models/'
    ml_models_directory = os.path.join(__script_dir, __rel_path)

    __rel_path = r'outputs/'
    output_directory = os.path.join(__script_dir, __rel_path)

    __rel_path = r'word_vectors/'
    word_vector_directory = os.path.join(__script_dir, __rel_path)

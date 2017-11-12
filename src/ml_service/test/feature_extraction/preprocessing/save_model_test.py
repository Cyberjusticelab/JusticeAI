import unittest
from src.ml_service.feature_extraction.preprocessing.save_model import save
import joblib
import os
from src.ml_service.global_variables.global_variable import Global

class TestStringMethods(unittest.TestCase):
    # to do
    def save(self):
        __script_dir = os.path.abspath(__file__ + r"/../")
        __processed_facts = 'processed_facts.bin'
        file_path = os.path.join(__script_dir, __processed_facts)
        Global.Precedence_Directory = __script_dir
        file = open('garbage.txt', 'w')
        file.writelines('[1] Le locateur est faible.\n')
        file.writelines('[2] Le locateur est faible.\n')
        file.writelines('[3] Le locateur est faible.\n')
        file.writelines('[4] Le locateur est faible.\n')
        file.writelines('[5] Le locateur est faible.\n')
        file.writelines('[6] Le chat veut me tuer.\n')
        file.writelines('[7] Le chat veut me tuer.\n')
        file.writelines('[8] Le chat veut me tuer.\n')
        file.writelines('[9] Le chat veut me tuer.\n')
        file.writelines('[10] Le chat veut me tuer.\n')
        file.close()
        save('facts', file_path, 1)

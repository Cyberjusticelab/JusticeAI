from src.ml_service.outputs.output import Log, Save
import unittest
import os
import joblib

class TestStringMethods(unittest.TestCase):
    def test_write(self):
        output_dir = os.path.abspath(__file__ + r"/../../../")
        rel_path = 'outputs/server.log'
        filename = os.path.join(output_dir, rel_path)
        Log.write('testing')
        file_found = os.path.isfile(filename)
        self.assertTrue(file_found)

    def test_binarize_model(self):
        output_dir = os.path.abspath(__file__ + r"/../../../")
        rel_path = 'outputs/test/test_model.bin'
        filename = os.path.join(output_dir, rel_path)
        s = Save('test')
        model = {'key': 'value'}
        s.binarize_model('test_model.bin', model)
        new_model = joblib.load(filename)
        self.assertEqual(new_model['key'], 'value')

    def test_save_text_file(self):
        output_dir = os.path.abspath(__file__ + r"/../../../")
        rel_path1 = 'outputs/test/test1.txt'
        filename1 = os.path.join(output_dir, rel_path1)

        rel_path2 = 'outputs/test/test2.txt'
        filename2 = os.path.join(output_dir, rel_path2)

        text1 = 'Goku will win the tournament of power.'
        text2 = ['Goku will win the tournament of power.', 'I love CC.']
        s = Save('test')
        s.save_text_file('test1.txt', text1, 'w')
        s.save_text_file('test2.txt', text2, 'w')

        self.assertTrue(os.path.isfile(filename1))
        self.assertTrue(os.path.isfile(filename2))

        test_str1 = ''
        file = open(filename1, 'r')
        for lines in file:
            test_str1 += lines.split('\n')[0]

        test_str2 = []
        file.close()
        file = open(filename2, 'r')
        for lines in file:
            test_str2.append(lines.split('\n')[0])
        file.close()
        self.assertEqual(test_str1, text1)
        self.assertEqual(test_str2, text2)
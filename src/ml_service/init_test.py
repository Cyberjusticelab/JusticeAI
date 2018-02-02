import os
import unittest
from util.constant import Path


class TestInitScript(unittest.TestCase):
    def test_init(self):
        import init
        self.assertTrue(os.path.isfile(Path.binary_directory + 'non-lem.bin'))
        self.assertTrue(os.path.isfile(Path.binary_directory + 'tenant_pays_landlord_scaler.bin'))
        self.assertTrue(os.path.isfile(Path.binary_directory + 'tenant_pays_landlord_regressor.bin'))
        self.assertTrue(os.path.isfile(Path.binary_directory + 'multi_class_svm_model.bin'))
        self.assertTrue(os.path.isfile(Path.binary_directory + 'classifier_labels.bin'))

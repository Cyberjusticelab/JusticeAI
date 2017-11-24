import unittest
from util.log import Log
import os


class TestLogger(unittest.TestCase):

    def test_write(self):
        filename = "server.log"
        Log.write("testing")
        root_directory = os.path.abspath(__file__ + r"/../../")
        full_path = os.path.join(root_directory, filename)
        file_found = os.path.isfile(full_path)
        self.assertTrue(file_found)

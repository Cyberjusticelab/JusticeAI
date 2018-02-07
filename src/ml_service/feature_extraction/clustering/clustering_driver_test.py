import unittest
from feature_extraction.clustering import clustering_driver
from util.constant import Path
import os


class TestClustering(unittest.TestCase):
    def test_kmeans(self):
        root_directory = os.path.abspath(__file__ + "r/../../../")
        __rel_path = r'data/test/mock_precedent/'
        test_data_directory = os.path.join(root_directory, __rel_path)

        __rel_path = r'data/raw/text_bk/'
        raw_data_directory = os.path.join(root_directory, __rel_path)

        Path.raw_data_directory = test_data_directory

        # k-means
        command_list = ["--kmeans", "--fact", "1"]
        self.assertTrue(clustering_driver.run(command_list))

        command_list = ["--kmeans", "--decision", "1"]
        self.assertTrue(clustering_driver.run(command_list))

        command_list = ["--kmeans", "--dwdw", "1"]
        self.assertTrue(not clustering_driver.run(command_list))

        command_list = ["--kmeans", "--decision", "string"]
        self.assertTrue(not clustering_driver.run(command_list))

        Path.raw_data_directory = raw_data_directory

    def test_dbscan(self):
        root_directory = os.path.abspath(__file__ + "r/../../../")
        __rel_path = r'data/test/mock_precedent/'
        test_data_directory = os.path.join(root_directory, __rel_path)

        __rel_path = r'data/raw/text_bk/'
        raw_data_directory = os.path.join(root_directory, __rel_path)

        Path.raw_data_directory = test_data_directory

        # dbscan
        command_list = ["--dbscan", "--fact", "1", "1"]
        self.assertTrue(clustering_driver.run(command_list))

        command_list = ["--dbscan", "--decision", "1", "1"]
        self.assertTrue(clustering_driver.run(command_list))

        command_list = ["--dbscan", "--dwdw", "1"]
        self.assertTrue(not clustering_driver.run(command_list))

        command_list = ["--dbscan", "--decision", "string"]
        self.assertTrue(not clustering_driver.run(command_list))

        Path.raw_data_directory = raw_data_directory

    def test_hdbscan(self):
        root_directory = os.path.abspath(__file__ + "r/../../../")
        __rel_path = r'data/test/mock_precedent/'
        test_data_directory = os.path.join(root_directory, __rel_path)

        __rel_path = r'data/raw/text_bk/'
        raw_data_directory = os.path.join(root_directory, __rel_path)

        Path.raw_data_directory = test_data_directory
        # dbscan
        command_list = ["--hdbscan", "--fact", "2", "1"]
        self.assertTrue(clustering_driver.run(command_list))

        command_list = ["--hdbscan", "--decision", "2", "1"]
        self.assertTrue(clustering_driver.run(command_list))

        command_list = ["--hdbscan", "--dwdw", "1"]
        self.assertTrue(not clustering_driver.run(command_list))

        command_list = ["--hdbscan", "--decision", "string"]
        self.assertTrue(not clustering_driver.run(command_list))

        Path.raw_data_directory = raw_data_directory

    def test_random_command(self):
        root_directory = os.path.abspath(__file__ + "r/../../../")
        __rel_path = r'data/test/mock_precedent/'
        test_data_directory = os.path.join(root_directory, __rel_path)

        __rel_path = r'data/raw/text_bk/'
        raw_data_directory = os.path.join(root_directory, __rel_path)

        Path.raw_data_directory = test_data_directory
        # bad command
        command_list = ["-random"]
        self.assertTrue(not clustering_driver.run(command_list))

        command_list = ["-random", 'ranndom']
        self.assertTrue(not clustering_driver.run(command_list))

        Path.raw_data_directory = raw_data_directory

import os
import shutil
import unittest
from io import BytesIO

from werkzeug.datastructures import FileStorage

from services import file_service


class FileServiceTest(unittest.TestCase):
    def test_file_service_path(self):
        path = file_service.generate_path(1, 1)
        self.assertTrue(path == '{}/conversations/{}/{}'.format(file_service.UPLOAD_FOLDER, 1, 1))

    def test_file_service_format(self):
        file = FileStorage(filename='my_file.pdf')
        self.assertTrue(file_service.is_accepted_format(file))

    def test_file_service_format_unsupported(self):
        file = FileStorage(filename='my_file.zip')
        self.assertFalse(file_service.is_accepted_format(file))

    def test_file_service_name_sanitize(self):
        file = FileStorage(filename='some/file/path/my_file.pdf')
        self.assertTrue(file_service.sanitize_name(file) == 'some_file_path_my_file.pdf')

    def test_file_service_upload(self):
        file_name = 'testfile.png'

        with open('test/testfile.png', 'rb') as f:
            stream = BytesIO(f.read())

        file = FileStorage(stream=stream, filename=file_name)
        file_name_sanitized = file_service.sanitize_name(file)
        file_path = file_service.generate_path(1, 1, testing=True)

        file_service.upload_file(file, file_path, file_name_sanitized)

        self.assertTrue(os.path.exists("{}/{}".format(file_path, file_name)))

        # Delete test upload folder
        shutil.rmtree("{}/".format(file_service.UPLOAD_FOLDER_TEST))

import os
import shutil
from io import BytesIO

from werkzeug.datastructures import FileStorage

from services import file_service
from services.static_strings import StaticStrings

"""
    Test for static response strings
    asserts that the proper static string of introduction is returned when "landlord" is selected by the user
"""


def test_static_strings():
    string = StaticStrings.chooseFrom(StaticStrings.problem_inquiry_landlord)
    assert string in StaticStrings.problem_inquiry_landlord


"""
    Test for file services
    asserts the functionality of the system for the upload of various files (zip, pdf, png images)
"""


def test_file_service_path():
    path = file_service.generate_path(1, 1)
    assert path == '{}/conversations/{}/{}'.format(file_service.UPLOAD_FOLDER, 1, 1)


def test_file_service_format():
    file = FileStorage(filename='my_file.pdf')
    assert file_service.is_accepted_format(file) is True


def test_file_service_format_unsupported():
    file = FileStorage(filename='my_file.zip')
    assert file_service.is_accepted_format(file) is False


def test_file_service_name_sanitize():
    file = FileStorage(filename='some/file/path/my_file.pdf')
    assert file_service.sanitize_name(file) == 'some_file_path_my_file.pdf'


def test_file_service_upload():
    file_name = 'testfile.png'

    with open('test/testfile.png', 'rb') as f:
        stream = BytesIO(f.read())

    file = FileStorage(stream=stream, filename=file_name)
    file_name_sanitized = file_service.sanitize_name(file)
    file_path = file_service.generate_path(1, 1, testing=True)

    file_service.upload_file(file, file_path, file_name_sanitized)

    assert os.path.exists("{}/{}".format(file_path, file_name))

    # Delete test upload folder
    shutil.rmtree("{}/".format(file_service.UPLOAD_FOLDER_TEST))

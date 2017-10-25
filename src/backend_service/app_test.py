from models.factService import FactService
from models.staticStrings import StaticStrings
from services import fileService


################
# staticStrings
################

def test_static_strings():
    string = StaticStrings.chooseFrom(StaticStrings.category_acknowledge)
    assert string in StaticStrings.category_acknowledge


###############
# factService
###############

def test_fact_service():
    fact, question = FactService.get_question('rent_change', [])
    assert fact == 'lease_term_type'
    assert question == "Is there a specified end date to your lease?"


def test_fact_service_empty():
    fact, question = FactService.get_question('rent_change',
                                              ['lease_term_type', 'is_rent_in_lease', 'rent_in_lease_amount'])
    assert fact is None
    assert question is None


###############
# fileService
###############

def test_file_service_path():
    path = fileService.generate_path(1, 1)
    assert path == '{}/conversations/{}/{}'.format(fileService.UPLOAD_FOLDER, 1, 1)


def test_file_service_format():
    file = TestFile(filename='my_file.pdf')
    assert fileService.is_accepted_format(file) is True


def test_file_service_format_unsupported():
    file = TestFile(filename='my_file.zip')
    assert fileService.is_accepted_format(file) is False


def test_file_service_name_sanitize():
    file = TestFile(filename='some/file/path/my_file.pdf')
    assert fileService.sanitize_name(file) == 'some_file_path_my_file.pdf'


###############
# Test Classes
###############

class TestFile:
    def __init__(self, filename):
        self.filename = filename

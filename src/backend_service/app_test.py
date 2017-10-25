from io import BytesIO

from models.factService import FactService
from models.staticStrings import StaticStrings
from services import fileService


def test_static_strings():
    str = StaticStrings.chooseFrom(StaticStrings.problem_inquiry)
    assert str in StaticStrings.problem_inquiry


def test_fact_service():
    fact, question = FactService.get_question('rent_change', [])
    assert fact == 'lease_term_type'
    assert question == "Is there a specified end date to your lease?"


def test_fact_service_empty():
    fact, question = FactService.get_question('rent_change',
                                              ['lease_term_type', 'is_rent_in_lease', 'rent_in_lease_amount'])
    assert fact is None
    assert question is None


def test_file_service_path():
    path = fileService.generate_path(1, 1)
    assert path == '{}/conversations/{}/{}'.format(fileService.UPLOAD_FOLDER, 1, 1)
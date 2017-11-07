from Taimoor_Parser import case
import os

c = case.Case(os.getcwd() + "/feature_extraction/Preprocessing/"
                            "Taimoor_Parser/dummy_cases/sample_case1.txt")


def test_no_demande():
    assert len(c.data["applicationID"]) == 1
    assert c.data["applicationID"][0] == "1234567"


def test_no_dossier():
    assert len(c.data["fileID"]) == 1
    assert c.data["fileID"][0] == "123456 12 12345678 D"


def test_total_hearings():
    assert c.data["totalHearings"] == 2


def test_is_rectified():
    assert c.data["isRectified"]

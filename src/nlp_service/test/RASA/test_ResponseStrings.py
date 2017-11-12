import pytest
from services import responseStrings


class test_ResponseStrings():

    def test_static_strings(self):
        string = responseStrings.chooseFrom(responseStrings.category_acknowledge)
        assert string in responseStrings.category_acknowledge

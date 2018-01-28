import unittest

from controllers import legal_controller


class LegalControllerTest(unittest.TestCase):
    def test_legal_controller(self):
        document_list = legal_controller.get_legal_documents()
        self.assertIsNotNone(document_list)

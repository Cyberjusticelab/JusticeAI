import unittest

from controllers import legal_controller

from backend_service.app import app


class LegalControllerTest(unittest.TestCase):
    def test_legal_controller(self):
        with app.test_request_context():
            document_list = legal_controller.get_legal_documents()
            self.assertIsNotNone(document_list)

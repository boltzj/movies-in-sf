import unittest
from app import create_app, db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_404(self):
        response = self.client.get('url/that/does/not/exist')
        self.assertTrue(response.status_code == 404)

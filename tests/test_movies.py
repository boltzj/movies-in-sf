import unittest
from app import create_app, db
from app.models.location import Location
from app.models.movie import Movie


class MovieTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_movie_404(self):
        response = self.client.get('movie/2147483647')
        self.assertTrue(response.status_code == 404)

    def test_get_movie_locations(self):
        response = self.client.get('movie/2147483647/locations')
        self.assertTrue(response.status_code == 404)

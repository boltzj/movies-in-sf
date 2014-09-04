from app import db
from googlegeocoder import GoogleGeocoder
import sys
import logging
import time

# Logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    fun_facts = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # Relations
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __init__(self, name, fun_facts, movie_id):
        self.name = name
        self.fun_facts = fun_facts
        self.movie_id = movie_id

    def get_information(self):
        return {
            'title': self.movie.title,
            'content': self.fun_facts,
            'location': self.name,
            'lat': self.latitude,
            'lng': self.longitude
        }

    def geocode(self, attempt):
        geocoder = GoogleGeocoder()

        try:
            logging.info('Try to geocode ' + self.name + ', San Francisco, CA')
            search = geocoder.get(self.name + ', San Francisco, CA')

            if search.__len__() > 0:
                logging.info(search)
                self.latitude = search[0].geometry.location.lat
                self.longitude = search[0].geometry.location.lng
            else:
                logging.info('No result for ' + self.name + ', San Francisco, CA')

            db.session.commit()

        except ValueError:
            # FIXME: Handle ValueError: OVER_QUERY_LIMIT (ValueError(data["status"])
            logging.warning('Google geocoder : ValueError')
            time.sleep(1)
            if attempt < 5:
                self.geocode(attempt + 1)
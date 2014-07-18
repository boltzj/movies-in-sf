__author__ = 'boltz_j'

import os
import json

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
config = os.path.join(app.root_path, 'config.cfg')
app.config.from_pyfile(config)

# Database init
db = SQLAlchemy(app)

# Movie SQLAlchemy model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    release_year = db.Column(db.Integer)
    production = db.Column(db.String(255))
    distributor = db.Column(db.String(255))
    # Foreign Keys
    locations = db.relationship('Location', backref='movie', lazy='dynamic')

    def __init__(self, title, release_year, production, distributor):
        self.title = title
        self.release_year = release_year
        self.production = production
        self.distributor = distributor


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    fun_facts = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __init__(self, name, fun_facts, movie_id):
        self.name = name
        self.fun_facts = fun_facts
        self.movie_id = movie_id


# Get a list of all movies names
@app.route('/movies', methods=['GET'])
def get_movies():

    # Get all movies from DB
    movies = Movie.query.all()

    result = []
    for movie in movies:
        result.append(movie.title)

    # return result as JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), result)


if __name__ == '__main__':
    app.run(debug=True)

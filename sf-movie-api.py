__author__ = 'boltz_j'

import os
import json
import time
import logging
import sys

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import cross_origin

from googlegeocoder import GoogleGeocoder

app = Flask(__name__)

# Database config
config = os.path.join(app.root_path, 'config.cfg')
app.config.from_pyfile(config)

# Database init
db = SQLAlchemy(app)

# Logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name


# Movie SQLAlchemy model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    release_year = db.Column(db.Integer)
    production = db.Column(db.String(255))
    distributor = db.Column(db.String(255))
    # Relationship
    locations = db.relationship('Location', backref='movie', lazy='dynamic')
    # Foreign Keys
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    actor1_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    actor2_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    actor3_id = db.Column(db.Integer, db.ForeignKey('actor.id'))

    def __init__(self, title, release_year, production, distributor):
        self.title = title
        self.release_year = release_year
        self.production = production
        self.distributor = distributor

    def add_director(self, director_id):
        self.director_id = director_id

    def add_writer(self, writer_id):
        self.writer_id = writer_id

    def add_actor1(self, actor1_id):
        self.actor1_id = actor1_id

    def add_actor2(self, actor2_id):
        self.actor2_id = actor2_id

    def add_actor3(self, actor3_id):
        self.actor3_id = actor3_id

    def to_json(self):
        return jsonify({
            'id': self.id,
            'Title': self.title,
            'Release Year': self.release_year,
            'Production Company': self.production,
            'Distributor': self.distributor,
            # 'locations : []
            # 'Director': director,
            # 'Writer': writer,
            # 'Actor 1': actor1,
            # 'Actor 2': actor2,
            # 'Actor 3': actor3,
        })


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


# Get a movie information
@app.route('/movie/<int:movie_id>', methods=['GET'])
@cross_origin()
def get_movie_by_id(movie_id):
    # Request DB for movie
    movie = Movie.query.get(movie_id)

    # FIXME : Handle 404 error
    return movie.to_json()


# Get a movie locations
@app.route('/movie/<int:movie_id>/locations', methods=['GET'])
@cross_origin()
def get_movie_locations(movie_id):
    # Request DB for movie
    locations = db.session.query(Location).filter(Location.movie_id == movie_id)

    result = []
    # FIXME : Handle 404 error
    for location in locations:
        movie = get_movie_by_id()
        result.append({
            'title': movie.title,
            'content': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get a list of all producers names
@app.route('/directors', methods=['GET'])
@cross_origin()
def get_directors():
    # Get all movies from DB
    directors = Director.query.all()

    result = []
    for director in directors:
        result.append(director.name)

    # return result as JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get all locations for a producer
@app.route('/producer/<int:producer_id>/locations', methods=['GET'])
@cross_origin()
def get_producer_locations(producer_id):
    # FIXME
    return producer_id + ' \n'


# Get a list of all writers names
@app.route('/writers', methods=['GET'])
@cross_origin()
def get_writers():
    # Get all movies from DB
    writers = Writer.query.all()

    result = []
    for writer in writers:
        result.append(writer.name)

    # return result as JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get all locations for a writer
@app.route('/writer/<int:writer_id>/locations', methods=['GET'])
@cross_origin()
def get_writer_locations(writer_id):
    # FIXME
    return writer_id + ' \n'


# Get a list of all actors names
@app.route('/actors', methods=['GET'])
@cross_origin()
def get_actors():
    # Get all movies from DB
    actors = Actor.query.all()

    result = []
    for actor in actors:
        result.append(actor.name)

    # return result as JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get all locations for an actor
@app.route('/actor/<int:actor_id>/locations', methods=['GET'])
@cross_origin()
def get_actor_locations(actor_id):
    # FIXME
    return actor_id + ' \n'


# Get all locations
@app.route('/locations', methods=['GET'])
@cross_origin()
def get_locations():
    locations = db.session.query(Location).join(Movie)

    result = []
    for location in locations:
        result.append({
            'movie_title': location.movie.title,
            'location_name': location.name,
            'fun_facts': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    return json.JSONEncoder.encode(json.JSONEncoder(), result)

if __name__ == '__main__':
    app.run(debug=True)

# Core
from app import db
from app.api import api
from flask import jsonify
from flask.ext.cors import cross_origin
# Models
from app.models.location import Location
from app.models.movie import Movie
# Utils
import random


def get_random_objects(cls, bulk=10):
    """
    :param cls: Class Object subclass of db.Model and implement get_information()
    :param bulk: Quantity of random objects (Default 10)
    :return:
    """
    # cls must be a subclass of a SQLAlchemy Model
    if not issubclass(cls, db.Model):
        raise ValueError
    # cls must have a method get_information
    if not callable(getattr(cls, "get_information", None)):
        raise ValueError

    # Get a random id with bulk size offset
    rand = random.randrange(bulk, cls.query.count()) + 1 - bulk

    # Store results object in a list
    results = []
    for object_id in range(rand, rand + bulk):
        # Get the object
        db_object = cls.query.get(object_id)
        # Add location information
        results.append(db_object)

    return results


@cross_origin()
@api.route('/random/locations', methods=['GET'])
def get_random_locations():
    """
    :return: Return some random locations
    """
    locations = []
    for location in get_random_objects(Location):
        locations.append(location.get_information())

    return jsonify(locations=locations)


@cross_origin()
@api.route('/random/movies', methods=['GET'])
def get_random_movies():
    """
    :return: Return some random movies
    """
    movies = []
    for movie in get_random_objects(Movie):
        movies.append(movie.get_information())

    return jsonify(movies=movies)


@cross_origin()
@api.route('/random/movies/locations', methods=['GET'])
def get_random_movies_location():
    """
    :return: Return some random movie locations
    """
    locations = []
    for movie in get_random_objects(Movie):
        for location in movie.locations:
            locations.append(location.get_information())

    return jsonify(locations=locations)

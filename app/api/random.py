# Core
from app import db
from app.api import api
from flask.ext.cors import cross_origin
from json import dumps
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
    result = []
    for object_id in range(rand, rand + bulk):
        # Get the object
        db_object = cls.query.get(object_id)
        # Add location information
        result.append(db_object)

    return result


@cross_origin()
@api.route('/random/locations', methods=['GET'])
def get_random_locations():
    """
    :return: Return some random locations
    """
    locations = []
    for location in get_random_objects(Location):
        locations.append(location.get_information())

    return dumps(locations)


@cross_origin()
@api.route('/random/movies', methods=['GET'])
def get_random_movies():
    """
    :return: Return some random movies
    """
    movies = []
    for movie in get_random_objects(Movie):
        movies.append(movie.get_information())

    return dumps(movies)


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

    return dumps(locations)

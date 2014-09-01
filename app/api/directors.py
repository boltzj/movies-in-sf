# Core
from app.api import api
from flask import abort
from flask.ext.cors import cross_origin
from urllib.parse import unquote
from json import dumps
# Models
from app.models.director import Director


@cross_origin()
@api.route('/directors', methods=['GET'])
def get_director_names():
    """
    Return all director names existing in the database
    :return: JSON with all director names
    """
    # Get all movies from DB
    directors = Director.query.all()

    # Store director names in an array
    director_names = []
    for director in directors:
        director_names.append(director.name)

    # return directors names in a JSON array string
    return dumps(director_names)


@cross_origin()
@api.route('/directors/<name>', methods=['GET'])
def get_director(name):
    """
    Return information about the director
    :param name of the director (URL encoded)
    :return: JSON with director information
    """
    # Get the director in the Database
    director = Director.query.filter(Director.name == unquote(name)).first()

    # If the director doesn't exist error 404
    if not director:
        return abort(404)

    # return director information in a JSON object
    return dumps(director.get_information())


@cross_origin()
@api.route('/directors/<name>/movies', methods=['GET'])
def get_director_movies(name):
    """
    Return the list all director's movies
    :param name of the director (URL encoded)
    :return: JSON with movies information
    """
    # Get the director in the Database
    director = Director.query.filter(Director.name == unquote(name)).first()

    # If the director doesn't exist error 404
    if not director:
        return abort(404)

    # Store director's movies in an array
    movies = []
    for movie in director.movies:
        movies.append(movie.get_information())

    # return movies in a JSON array
    return dumps(movies)


@cross_origin()
@api.route('/directors/<name>/locations', methods=['GET'])
def get_director_locations(name):
    """
    Return the list of all locations linked to a director
    :param name of the director (URL encoded)
    :return: JSON with locations
    """
    # Get the director in the Database
    director = Director.query.filter(Director.name == unquote(name)).first()

    # If the director doesn't exist error 404
    if not director:
        return abort(404)

    # Store the locations in an array
    locations = []
    for movie in director.movies:
        for location in movie.locations:
            locations.append(location.get_information())

    # return locations in a JSON array
    return dumps(locations)

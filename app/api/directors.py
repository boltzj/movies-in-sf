# Core
from app.api import api
from flask import json, abort
from flask.ext.cors import cross_origin
from urllib.parse import unquote
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

    # return directors names in a JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), director_names)


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

    director_info = {
        'name': director.name
    }

    # return director information in a JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), director_info)


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
        movies.append({
            'title': movie.title,
            'year': movie.release_year,
        })

    # return movies in a JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), movies)


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
            locations.append({
                'title': movie.title,
                'content': location.fun_facts,
                'location': location.name,
                'lat': location.latitude,
                'lng': location.longitude
            })

    # return locations in a JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), locations)

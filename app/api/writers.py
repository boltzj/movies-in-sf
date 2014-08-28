# Core
from app.api import api
from flask import json, abort
from flask.ext.cors import cross_origin
from urllib.parse import unquote
# Models
from app.models.writer import Writer


@cross_origin()
@api.route('/writers', methods=['GET'])
def get_writer_names():
    """
    Return all writer names existing in the database
    :return: JSON with all writer names
    """
    # Get all movies from DB
    writers = Writer.query.all()

    # Store writer names in an array
    writers_names = []
    for writer in writers:
        writers_names.append(writer.name)

    # return writers names in a JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), writers_names)


@cross_origin()
@api.route('/writers/<name>', methods=['GET'])
def get_writer(name):
    """
    Return information about the writer
    :param name of the writer (URL encoded)
    :return: JSON with writer information
    """
    # Get the writer in the Database
    writer = Writer.query.filter(Writer.name == unquote(name)).first()

    # If the writer doesn't exist error 404
    if not writer:
        return abort(404)

    writer_info = {
        'name': writer.name
    }

    # return writer information in a JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), writer_info)


@cross_origin()
@api.route('/writers/<name>/movies', methods=['GET'])
def get_writer_movies(name):
    """
    Return the list all writer's movies
    :param name of the writer (URL encoded)
    :return: JSON with movies information
    """
    # Get the writer in the Database
    writer = Writer.query.filter(Writer.name == unquote(name)).first()

    # If the writer doesn't exist error 404
    if not writer:
        return abort(404)

    # Store writer's movies in an array
    movies = []
    for movie in writer.movies:
        movies.append({
            'title': movie.title,
            'year': movie.release_year,
        })

    # return movies in a JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), movies)


@cross_origin()
@api.route('/writers/<name>/locations', methods=['GET'])
def get_writer_locations(name):
    """
    Return the list of all locations linked to a writer
    :param name of the writer (URL encoded)
    :return: JSON with locations
    """
    # Get the writer in the Database
    writer = Writer.query.filter(Writer.name == unquote(name)).first()

    # If the writer doesn't exist error 404
    if not writer:
        return abort(404)

    # Store the locations in an array
    locations = []
    for movie in writer.movies:
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

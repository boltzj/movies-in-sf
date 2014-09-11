# Core
from app.api import api
# Models
from app.models.movie import Movie
# Utils
from flask import abort, jsonify
from flask.ext.cors import cross_origin
from urllib.parse import unquote


@cross_origin()
@api.route('/movies', methods=['GET'])
def get_movie_names():
    """
    Return all movie names existing in the database
    :return: JSON with all movie names
    """
    # Get all movies from DB
    movies = Movie.query.all()

    # Store movie names in an array
    movie_names = []
    for movie in movies:
        movie_names.append(movie.name)

    # return movies names in a JSON array string
    return jsonify(names=movie_names)


@cross_origin()
@api.route('/movies/<name>', methods=['GET'])
def get_movie(name):
    """
    Return information about the movie
    :param name of the movie (URL encoded)
    :return: JSON with movie information
    """
    # Get the movie in the Database
    movie = Movie.query.filter(Movie.name == unquote(name)).first()

    # If the movie doesn't exist error 404
    if not movie:
        return abort(404)

    # return movie information in a JSON object
    return jsonify(movie=movie.get_information())


@cross_origin()
@api.route('/movies/<name>/locations', methods=['GET'])
def get_movie_locations(name):
    """
    Return the list of all locations linked to a movie
    :param name of the movie (URL encoded)
    :return: JSON with locations
    """
    # Get the movie in the Database
    movie = Movie.query.filter(Movie.name == unquote(name)).first()

    # If the movie doesn't exist error 404
    if not movie:
        return abort(404)

    # Store the locations in an array
    locations = []
    for location in movie.locations:
        locations.append(location.get_information())

    # return locations in a JSON array
    return jsonify(locations=locations)

# Core
from app.api import api
from flask.ext.cors import cross_origin
# Models
from app.models.movie import Movie
# Utils
from flask import abort
from urllib.parse import unquote
from json import dumps


@cross_origin()
@api.route('/movies', methods=['GET'])
def get_movie_titles():
    """
    Return all movie titles existing in the database
    :return: JSON with all movie titles
    """
    # Get all movies from DB
    movies = Movie.query.all()

    # Store movie titles in an array
    movie_titles = []
    for movie in movies:
        movie_titles.append(movie.title)

    # return movies titles in a JSON array string
    return dumps(movie_titles)


@cross_origin()
@api.route('/movies/<title>', methods=['GET'])
def get_movie(title):
    """
    Return information about the movie
    :param title of the movie (URL encoded)
    :return: JSON with movie information
    """
    # Get the movie in the Database
    movie = Movie.query.filter(Movie.title == unquote(title)).first()

    # If the movie doesn't exist error 404
    if not movie:
        return abort(404)

    # return movie information in a JSON object
    return dumps(movie.get_information())


@cross_origin()
@api.route('/movies/<title>/locations', methods=['GET'])
def get_movie_locations(title):
    """
    Return the list of all locations linked to a movie
    :param title of the movie (URL encoded)
    :return: JSON with locations
    """
    # Get the movie in the Database
    movie = Movie.query.filter(Movie.title == unquote(title)).first()

    # If the movie doesn't exist error 404
    if not movie:
        return abort(404)

    # Store the locations in an array
    locations = []
    for location in movie.locations:
        locations.append(location.get_information())

    # return locations in a JSON array
    return dumps(locations)

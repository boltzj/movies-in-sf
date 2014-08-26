import json

# Core
from app.api import api
from flask.ext.cors import cross_origin

# Models
from app.models.movie import Movie

# Utils
from flask import request


@api.route('/movies', methods=['GET'])
@cross_origin()
def get_movies_titles():
    """
    Return a list of all movies titles
    """
    # Get all movies from DB
    movies = Movie.query.all()

    # Store the movies title in an array
    result = []
    for movie in movies:
        result.append(movie.title)

    return json.JSONEncoder.encode(json.JSONEncoder(), result)


@api.route('/movie/<int:movie_id>', methods=['GET'])
@cross_origin()
def get_movie_by_id(movie_id):
    """
    Return the information about a movie
    :param movie_id:
    :return: movie information
    """
    # Request DB for movie or raise 404 Error
    movie = Movie.query.get_or_404(movie_id)

    return movie.to_json()


@api.route('/movie/<int:movie_id>/locations', methods=['GET'])
@cross_origin()
def get_movie_locations(movie_id):
    """
    Get all locations for a movie
    """
    # Request DB for movie or raise 404 Error
    movie = Movie.query.get_or_404(movie_id)

    # Store the location in an array
    result = []
    for location in movie.locations:
        result.append({
            'title': movie.title,
            'location': location.name,
            'content': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    return json.JSONEncoder.encode(json.JSONEncoder(), result)


@api.route('/movie/name', methods=['GET'])
@cross_origin()
def search_locations_by_movie_name():
    """
    Take a name of a movie and return all location for a movie
    :return:
    """
    query = request.args.get('q')

    # Get all movies from DB
    movies = Movie.query.filter(Movie.title == query)

    result = []
    for movie in movies:
        result.append({'id': movie.id})

    if len(result) == 1:
        return get_movie_locations(result[0]['id'])
    else:
        # empty or more than one
        return json.JSONEncoder.encode(json.JSONEncoder(), result)

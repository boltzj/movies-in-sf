import json

# Core
from . import api
from app import db
from flask.ext.cors import cross_origin

# Models
from app.models.movie import Movie
from app.models.location import Location

# Utils
from flask import jsonify, request


@api.route('/movies', methods=['GET'])
@cross_origin()
def get_movies():
    # Get all movies from DB
    movies = Movie.query.all()

    result = []
    for movie in movies:
        result.append(movie.title)

    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get a movie information
@api.route('/movie/<int:movie_id>', methods=['GET'])
@cross_origin()
def get_movie_by_id(movie_id):
    # Request DB for movie
    movie = Movie.query.get(movie_id)

    # FIXME : Handle 404 error
    return movie.to_json()


# Get a movie locations
@api.route('/movie/<int:movie_id>/locations', methods=['GET'])
@cross_origin()
def get_movie_locations(movie_id):
    # Request DB for movie
    locations = db.session.query(Location).join(Movie).filter(Location.movie_id == movie_id)

    result = []
    # FIXME : Handle 404 error
    for location in locations:
        result.append({
            'title': location.movie.title,
            'location': location.name,
            'content': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get a list of all location for a movie
@api.route('/movie/name', methods=['GET'])
@cross_origin()
def search_locations_by_movie_name():
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

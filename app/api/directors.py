# Core
from . import api
from flask import json, request
from app import db
from flask.ext.cors import cross_origin

# Models
from app.models.director import Director
from app.models.location import Location
from app.models.movie import Movie


# Get a list of all directors names
@api.route('/directors', methods=['GET'])
@cross_origin()
def get_directors():
    # Get all movies from DB
    directors = Director.query.all()

    result = []
    for director in directors:
        result.append(director.name)

    # return result as JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get all locations for a director
@api.route('/director/<int:director_id>/locations', methods=['GET'])
@cross_origin()
def get_director_locations(director_id):

    locations = db.session.query(Location).join(Movie).join(Director).filter(Director.id == director_id)

    result = []
    for location in locations:
        result.append({
            'title': location.movie.title,
            'location': location.name,
            'content': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get a list of all location for a director
@api.route('/director/name', methods=['GET'])
@cross_origin()
def search_locations_by_director_name():
    query = request.args.get('q')

    # Get all movies from DB
    directors = Director.query.filter(Director.name == query)

    result = []
    for director in directors:
        result.append({'id': director.id})

    if len(result) == 1:
        return get_director_locations(result[0]['id'])
    else:
        # empty or more than one
        return json.JSONEncoder.encode(json.JSONEncoder(), result)

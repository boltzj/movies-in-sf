# Core
from . import api
from flask import json, request
from app import db
from flask.ext.cors import cross_origin

# Models
from app.models.actor import Actor
from app.models.location import Location
from app.models.movie import Movie


# Get a list of all actors names
@api.route('/actors', methods=['GET'])
@cross_origin()
def get_actors():
    # Get all movies from DB
    actors = Actor.query.all()

    result = []
    for actor in actors:
        result.append(actor.name)

    # return result as JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), result)

# Get a list of all location for an actor
@api.route('/actor/name', methods=['GET'])
@cross_origin()
def search_locations_by_actor_name():
    query = request.args.get('q')

    # Get all movies from DB
    actors = Actor.query.filter(Actor.name == query)

    result = []
    for actor in actors:
        result.append({'id': actor.id})

    if len(result) == 1:
        return get_actor_locations(result[0]['id'])
    else:
        # empty or more than one
        return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get all locations for an actor
@api.route('/actor/<int:actor_id>/locations', methods=['GET'])
@cross_origin()
def get_actor_locations(actor_id):

    result = []

    locations = db.session.query(Location)\
        .join(Movie)\
        .join(Actor, Movie.actor1_id == Actor.id)\
        .filter(Actor.id == actor_id)
    for location in locations:
        result.append({
            'title': location.movie.title,
            'location': location.name,
            'content': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    locations = db.session.query(Location)\
        .join(Movie)\
        .join(Actor, Movie.actor2_id == Actor.id)\
        .filter(Actor.id == actor_id)
    for location in locations:
        result.append({
            'title': location.movie.title,
            'location': location.name,
            'content': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    locations = db.session.query(Location)\
        .join(Movie)\
        .join(Actor, Movie.actor3_id == Actor.id)\
        .filter(Actor.id == actor_id)
    for location in locations:
        result.append({
            'title': location.movie.title,
            'location': location.name,
            'content': location.fun_facts,
            'lat': location.latitude,
            'lng': location.longitude
        })

    return json.JSONEncoder.encode(json.JSONEncoder(), result)

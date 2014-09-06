# Core
from app.api import api
from flask import abort, jsonify
from flask.ext.cors import cross_origin
from urllib.parse import unquote
from json import dumps
# Models
from app.models.actor import Actor


@cross_origin()
@api.route('/actors', methods=['GET'])
def get_actor_names():
    """
    Return all actor name existing in the database
    :return: List of all actors names
    """
    # Get all actors from DB
    actors = Actor.query.all()

    # Store actor names in an array
    actor_names = []
    for actor in actors:
        actor_names.append(actor.name)

    # return actor names in a JSON array
    return jsonify(names=actor_names)


@cross_origin()
@api.route('/actors/<name>', methods=['GET'])
def get_actor(name):
    """
    Return information about the actor
    :param name of the actor (URL encoded)
    :return: JSON with actor information
    """
    # Get the actor in the Database
    actor = Actor.query.filter(Actor.name == unquote(name)).first()

    # If the actor doesn't exist return 404
    if not actor:
        return abort(404)

    # return actor information in a JSON object
    return jsonify(actor=actor.get_information())


@cross_origin()
@api.route('/actors/<name>/movies', methods=['GET'])
def get_actor_movies(name):
    """
    Return the list all actor's movies
    :param name of the actor (URL encoded)
    :return: JSON with movies information
    """
    # Get the actor in the Database
    actor = Actor.query.filter(Actor.name == unquote(name)).first()

    # If the actor doesn't exist error 404
    if not actor:
        return abort(404)

    # Store actor's movies in an array
    movies = []
    for movie in actor.movies:
        movies.append(movie.get_information())

    # return movies in a JSON array
    return jsonify(movies=movies)


@cross_origin()
@api.route('/actors/<name>/locations', methods=['GET'])
def get_actor_locations(name):
    """
    Return the list of all locations linked to a actor
    :param name of the actor (URL encoded)
    :return: JSON with locations
    """
    # Get the actor in the Database
    actor = Actor.query.filter(Actor.name == unquote(name)).first()

    # If the actor doesn't exist error 404
    if not actor:
        return abort(404)

    # Store the locations in an array
    locations = []
    for movie in actor.movies:
        for location in movie.locations:
            locations.append(location.get_information())

    # return locations in a JSON array
    return jsonify(locations=locations)

# Core
from . import api
from flask import json, request
from app import db
from flask.ext.cors import cross_origin

# Models
from app.models.writer import Writer
from app.models.location import Location
from app.models.movie import Movie

# Get a list of all writers names
@api.route('/writers', methods=['GET'])
@cross_origin()
def get_writers():
    # Get all movies from DB
    writers = Writer.query.all()

    result = []
    for writer in writers:
        result.append(writer.name)

    # return result as JSON array
    return json.JSONEncoder.encode(json.JSONEncoder(), result)


# Get all locations for a writer
@api.route('/writer/<int:writer_id>/locations', methods=['GET'])
@cross_origin()
def get_writer_locations(writer_id):
    locations = db.session.query(Location).join(Movie).join(Writer).filter(Writer.id == writer_id)

    result = []
    for location in locations:
        result.append({
            'title': location.movie.title,
            'content': location.fun_facts,
            'location': location.name,
            'lat': location.latitude,
            'lng': location.longitude
        })

    return json.JSONEncoder.encode(json.JSONEncoder(), result)

# Get a list of all location for a writer
@api.route('/writer/name', methods=['GET'])
@cross_origin()
def search_locations_by_writer_name():
    query = request.args.get('q')

    # Get all movies from DB
    writers = Writer.query.filter(Writer.name == query)

    result = []
    for writer in writers:
        result.append({'id': writer.id})

    if len(result) == 1:
        return get_writer_locations(result[0]['id'])
    else:
        # empty or more than one
        return json.JSONEncoder.encode(json.JSONEncoder(), result)

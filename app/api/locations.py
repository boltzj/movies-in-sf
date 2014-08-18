# Core
from . import api
from flask import json
from app import db
from flask.ext.cors import cross_origin

# Models
from app.models.location import Location
from app.models.movie import Movie


# Get all locations
@api.route('/locations', methods=['GET'])
@cross_origin()
def get_locations():
    locations = db.session.query(Location).join(Movie)

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

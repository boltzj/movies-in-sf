# Core
from app.api import api
from flask import json
from flask.ext.cors import cross_origin

# Models
from app.models.location import Location


@api.route('/locations', methods=['GET'])
@cross_origin()
def get_locations():
    """
    :return: Return a list with all locations
    """
    # Get all movies from DB
    locations = Location.query.all()

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

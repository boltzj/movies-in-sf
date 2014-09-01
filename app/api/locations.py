# Core
from app.api import api
from flask.ext.cors import cross_origin
from json import dumps
# Models
from app.models.location import Location


@cross_origin()
@api.route('/locations', methods=['GET'])
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

    return dumps(result)

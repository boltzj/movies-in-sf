from app.api import api
from flask import jsonify


@api.errorhandler(404)
def not_found(e):
    response = jsonify({'error': e.name, 'description': e.description})
    response.status_code = e.code
    return response

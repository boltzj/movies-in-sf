from flask import jsonify


def not_found():
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response

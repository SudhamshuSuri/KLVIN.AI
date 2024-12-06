from flask import jsonify

def create_response(data, status=200):
    response = jsonify(data)
    response.status_code = status
    return response


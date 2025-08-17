from flask import jsonify

def success_response(status_code, message, data=None):
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(status_code, message):
    response = {
        "status": "error",
        "message": message
    }
    return jsonify(response), status_code

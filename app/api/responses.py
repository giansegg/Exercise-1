from flask import jsonify

def success_response(data):
    return jsonify({"status": "success", "data": data})

def error_response(message):
    return jsonify({"status": "error", "message": message})

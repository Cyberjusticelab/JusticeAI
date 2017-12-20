from flask import request, make_response, jsonify

def ensure_json(func):
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return make_response(jsonify(message='Only application/json supported'), 415)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def ensure_key(key):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not key in request.get_json():
                return make_response(jsonify(message='\'question\' key is required'), 422)
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


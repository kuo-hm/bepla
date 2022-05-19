
from functools import wraps

from flask import current_app, jsonify, request
from jwt import decode


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            
            userData = decode(token.encode(
                "UTF-8"),  current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(userData, *args, **kwargs)
    return decorated

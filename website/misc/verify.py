from jwt import  decode
from jwt import exceptions
from datetime import datetime, timedelta
from flask import jsonify,current_app

def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date




def validate_token(token, output=False):
    try:
        if output:
            return decode(token.encode("UTF-8"), key=current_app.config["SECRET_KEY"], algorithms=["HS256"])
        decode(token, key= current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response


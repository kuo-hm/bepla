from os import access

from flask import Blueprint, current_app, request
from flask.json import jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies)
from website import db
from website.misc.HttpMethods import HttpMethods

Test = Blueprint("Test", __name__)


@Test.route('/test', methods=[HttpMethods.GET.value])
def test():
    refresh = create_refresh_token(identity="used")
    access_token = create_access_token(identity="example_user")
    token={
        'access_token':access_token,
        'refresh_token':refresh
    }
    response = jsonify(token)
    return response

@Test.route('/refresh', methods=[HttpMethods.GET.value])
@jwt_required(refresh=True)
def test2():
    identity=get_jwt_identity()
    access_token = create_access_token(identity=identity)
    refresh = create_refresh_token(identity=identity)
    token={
        'access_token':access_token,
        'refresh_token':refresh
    }
    response = jsonify(token)
    return response

@Test.route('/protected', methods=[HttpMethods.GET.value])
@jwt_required()
def protected():
    identity=get_jwt_identity()

    return jsonify(foo=identity)


from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, current_app, request
from flask.json import jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies)
from jwt import encode
from website.decorators.verify import token_required
from website.misc.HttpMethods import HttpMethods
from website.misc.verify import validate_token
from website.model.user import User

auth = Blueprint("auth", __name__)


def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date

# ------------------------------------------------------------------------------
# -----------------------------ROUTES-------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                              Login
# ------------------------------------------------------------------------------
@auth.route("/login", methods=[HttpMethods.POST.value])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if not email or not password:
        return jsonify({'message': 'Please provide email and password!', "fail": True})
    user = User.login(email, password)
    if user:
        refresh = create_refresh_token(identity={"email": email, "name": user.username, "id": user.id})
        access_token = create_access_token(identity={"email": email, "name": user.username, "id": user.id})
        token={
            'refresh_token':refresh,
            'access_token':access_token
            
             }
        response = jsonify({"token": token, "fail": False})
        set_access_cookies(response=response, access_token=access_token)
        return jsonify({"token": token, "fail": False})
    else:
        response = jsonify({"message": "Wrong credentials", "fail": True})
        return response


# ------------------------------------------------------------------------------
#                              Register
# ------------------------------------------------------------------------------
@auth.route("/signup", methods=[HttpMethods.POST.value])
def sign_up():
    try:
        data = request.get_json()
        username = data['name']
        email = data['email']
        password2 = data['passwordConfirm']
        password = data['password']
        email_exists = User.check_email(email)
        if email_exists:
            response = jsonify(
                {"message": "Email already exists", "fail": True})
            return response
        elif not username or not email or not password or not password2:
            response = jsonify(
                {"message": "Please fill all fields", "fail": True})
            return response
        elif password != password2:
            response = jsonify(
                {"message": "Passwords do not match", "fail": True})
            return response
        elif len(username) < 2:
            response = jsonify(
                {"message": "Username is too short", "fail": True})
            return response
        elif len(password) < 6:
            response = jsonify(
                {"message": "Password is too short", "fail": True})
            return response
        elif len(email) < 4:
            response = jsonify({"message": "Email is too short", "fail": True})
            return response
        else:
            user = User.signup(username, email, password)
            print(user)
            if user:
                response = jsonify(
                    {"message": "User created successfully", "fail": False})
                response.status_code = 201
                return response
            else:
                response = jsonify(
                    {"message": "Something went wrong", "fail": True})
                response.status_code = 400
                return response
    except Exception as e:
        response = jsonify({"message": str(e), "fail": True})
        response.status_code = 404
        return response

# ------------------------------------------------------------------------------
#                              Change Password
# ------------------------------------------------------------------------------


@auth.route("/change_password", methods=[HttpMethods.PUT.value])
@jwt_required()
def change_password():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        new_password = data['new_password']
        user = User.change_password(email, password, new_password)
        if user:
            response = jsonify({"message": "Password changed successfully"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Wrong credentials"})
            response.status_code = 404
            return response
    except Exception as e:
        response = jsonify({"message": "Something went wrong"})
        response.status_code = 404
        return response


# ------------------------------------------------------------------------------
#                              Change Email
# ------------------------------------------------------------------------------
@auth.route("/change_email", methods=[HttpMethods.PUT.value])
@jwt_required()
def change_email():
    try:
        data = request.get_json()
        email = data['email']
        new_email = data['new_email']
        password = data['password']
        if new_email == email:
            return jsonify({"message": "Email already exists"})
        user = User.change_email(email, password, new_email)
        if user:
            response = jsonify({"message": "Email changed successfully"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Wrong credentials"})
            response.status_code = 404
            return response
    except Exception as e:
        response = jsonify({"message": "Something went wrong"})
        response.status_code = 404
        return response


# ------------------------------------------------------------------------------
#                              Change Username
# ------------------------------------------------------------------------------
@auth.route("/change_profile", methods=[HttpMethods.PUT.value])
@jwt_required()
def change_username():
    try:
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = data['password']
        new_username = data['new_username']
        user = User.change_username(email, password, new_username)
        if username == new_username:
            response = jsonify({"message": "Username already exists"})
            response.status_code = 200
            return response
        if user:
            response = jsonify({"message": "Username changed successfully"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Wrong credentials"})
            response.status_code = 404
            return response
    except Exception as e:
        response = jsonify({"message": "Something went wrong"})
        response.status_code = 404
        return response


# ------------------------------------------------------------------------------
#                              Change Avatar
# ------------------------------------------------------------------------------
@auth.route("/change_avatar", methods=[HttpMethods.POST.value])
@jwt_required()
def change_avatar():
    return jsonify({"message": "Not implemented yet"})


# ------------------------------------------------------------------------------
#                           Add Social Media
# ------------------------------------------------------------------------------
@auth.route("/add_social_links", methods=[HttpMethods.POST.value])
@jwt_required()
def add_social_links():
    return jsonify({"message": "Not implemented yet"})


# ------------------------------------------------------------------------------
#                              Refresh Token
# ------------------------------------------------------------------------------
@auth.route('/token/refresh', methods=[HttpMethods.POST.value])
@jwt_required(refresh=True)
def refresh():
    identity=get_jwt_identity()
    access_token = create_access_token(identity=identity)
    refresh = create_refresh_token(identity=identity)
    token={
        'access_token':access_token,
        'refresh_token':refresh
    }
    response = jsonify(token)
    return response

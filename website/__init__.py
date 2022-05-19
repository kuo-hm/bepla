import pathlib
from os import path

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
db = SQLAlchemy()
DB_NAME = "database.db"


app = Flask(__name__, instance_relative_config=True)

app.config['UPLOAD_VIDEO'] = pathlib.Path(
    __file__).parent.resolve()/'Data'/'upload'/'videos'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///Data/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['JWT_SECRET_KEY'] = "sqdsddfzaedqsdxqzecqsdqx"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=3)


jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

def create_app():
    # app = Flask(__name__,static_folder=path.dirname(__file__)+"beform/dist",template_folder="../dist")
    db.init_app(app)
    from .views.auth.auth import auth
    from .views.cart.cart import cart
    from .views.courses.courses import courses
    from .views.testjwt.test import Test
    from .views.tracker.Track import Track

    # from .views.certif import certif
    # app.register_blueprint(certif, url_prefix="/")
    app.register_blueprint(courses, url_prefix="/api/courses")
    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(cart, url_prefix="/api/cart")
    app.register_blueprint(Track, url_prefix="/api/track")

    app.register_blueprint(Test, url_prefix="/test")

    create_database(app)

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")

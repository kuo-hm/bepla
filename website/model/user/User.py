import uuid
from datetime import datetime

from sqlalchemy.sql import func
from website import db
from werkzeug.security import check_password_hash, generate_password_hash


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(32), primary_key=True,
                   unique=True, default=generate_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    role = db.Column(db.Integer, default=0, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    avatar = db.Column(db.Text, default='default.png')

    facebook = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    google = db.Column(db.String(150))
    github = db.Column(db.String(150))
    linkedin = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    youtube = db.Column(db.String(150))
    about = db.Column(db.Text)

    def hash_passowrd(password):
        return generate_password_hash(
            password, method='sha256')

    def check_password(password, hash):
        return check_password_hash(
            hash, password)

    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if user and User.check_password(password, user.password):
            return user
        return False

    def change_password(username, password, new_password):
        user: User = User.query.filter_by(username=username).first()
        if user and User.check_password(password, user.password):
            user.password = User.hash_passowrd(new_password)
            user.save()
            return user
        return False

    def change_email(email, password, new_email):
        user: User = User.query.filter_by(email=email).first()
        if user and User.check_password(password, user.password):
            user.email = new_email
            user.save()
            return user
        return False

    def check_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        return False

    def change_username(email: str, password: str, new_username: str):
        user: User = User.query.filter_by(email=email).first()
        if user and User.check_password(password, user.password):
            user.username = new_username
            user.save()
            return user
        return False

    def change_avatar(email, password, new_avatar):
        user: User = User.query.filter_by(email=email).first()
        if user and User.check_password(password, user.password):
            user.avatar = new_avatar
            user.save()
            return user
        return False

    def signup(username, email, password):
        user = User(
            username=username,
            email=email,
            password=User.hash_passowrd(password)
        )
        print(username, email, password)
        db.session.add(user)
        db.session.commit()
        return user

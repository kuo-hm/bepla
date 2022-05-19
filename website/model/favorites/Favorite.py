from sqlalchemy.sql import func
from website import db


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def get_favourites(user_id, course_id):
        favourite = Favorite.query.filter_by(
            user_id=user_id, course_id=course_id).first()
        if favourite:
            return True
        else:
            return False

    def toggle_favourite(user_id, course_id):
        favourite = Favorite.query.filter_by(
            user_id=user_id, course_id=course_id).first()
        if favourite:
            db.session.delete(favourite)
        else:
            new_favourite = Favorite(user_id=user_id, course_id=course_id)
            db.session.add(new_favourite)

        db.session.commit()
        return True

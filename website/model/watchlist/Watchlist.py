from sqlalchemy.sql import func
from website import db


class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    watchtime = db.Column(db.Integer, nullable=True)
    lessons_id = db.Column(db.Integer, db.ForeignKey(
        'lessons.id', ondelete="CASCADE"), nullable=True)
    finished = db.Column(db.Boolean, nullable=True, default=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id', ondelete="CASCADE"), nullable=False)

    def add_to_watchlist(lessons_id, user_id, watchtime, finished, course_id):
        new_watchlist = Watchlist(lessons_id=lessons_id, course_id=course_id, user_id=user_id,
                                  watchtime=watchtime, finished=finished)
        db.session.add(new_watchlist)
        db.session.commit()

    def watched(course_id, user_id):
        watched = Watchlist.query.filter_by(
            course_id=course_id, user_id=user_id).first()
        if watched:
            return True
        else:
            return False

    def track_click(course_id, user_id):
        watched = Watchlist.watched(course_id, user_id)
        if watched:
            return False
        else:
            new_click = Watchlist(course_id=course_id,  user_id=user_id,
                                  watchtime=0, finished=False)
            db.session.add(new_click)
            db.session.commit()
            return True

    def remove_click(course_id, user_id):
        watched = Watchlist.watched(course_id, user_id)
        if watched:
            db.session.query(Watchlist).filter_by(
                course_id=course_id, user_id=user_id).delete()
            db.session.commit()
            return True
        else:
            return False

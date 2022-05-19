from sqlalchemy.sql import func
from website import db


class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id', ondelete="CASCADE"), nullable=False)
    lesson_name = db.Column(db.String(150), nullable=False)
    lesson_order = db.Column(db.Integer, nullable=False)
    lesson_column = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    video = db.relationship('Video', backref='lessons',
                            passive_deletes=True, uselist=False, )
    watchlist = db.relationship(
        'Watchlist', backref='lessons', passive_deletes=True)

    def add_lesson(data):
        course_id = data['course_id']
        lesson_name = data['lesson_name']
        lesson_content = data['lesson_content']
        lesson_duration = data['lesson_duration']
        lesson_order = data['lesson_order']
        lesson_column = data['lesson_column']
        lesson = Lessons(course_id=course_id, lesson_name=lesson_name, lesson_content=lesson_content,
                         lesson_duration=lesson_duration, lesson_order=lesson_order, lesson_column=lesson_column)
        db.session.add(lesson)
        return lesson

    def get_lesson(id):
        return Lessons.query.filter_by(id=id).first()

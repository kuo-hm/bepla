from sqlalchemy.sql import func
from website import db


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), unique=True)
    course_image = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    course_description = db.Column(db.Text, nullable=False)
    course_preview = db.Column(db.String(150), nullable=False)
    course_content = db.Column(db.Text, nullable=False)
    course_price = db.Column(db.Integer, nullable=False)
    course_duration = db.Column(db.Integer, nullable=False)
    course_category = db.Column(db.String(150), nullable=False)
    course_free = db.Column(db.Boolean, nullable=False, default=False)
    # user_id = db.Column(db.String, db.ForeignKey(
    #     'user.id', ondelete="CASCADE"), nullable=True)

    def check_course(course_name: str):
        course = Course.query.filter_by(course_name=course_name).first()
        if course:
            return True
        return False

    def add_courses(data):
        course_name = data['course_name']
        course_image = data['course_image']
        course_author = data['course_author']
        course_description = data['course_description']
        course_preview = data['course_preview']
        course_content = data['course_content']
        course_price = data['course_price']
        course_duration = data['course_duration']
        course_category = data['course_category']
        course_free = data['course_free']
        course = Course(course_name=course_name, course_image=course_image, author=course_author, course_description=course_description, course_preview=course_preview,
                        course_content=course_content, course_price=course_price, course_duration=course_duration, course_category=course_category, course_free=course_free)
        db.session.add(course)
        db.session.commit()
        return course

    def get_courses():
        return Course.query.all()

    def get_course(id):
        return Course.query.filter_by(id=id).first()

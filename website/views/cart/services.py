
from flask.json import jsonify
from website.model import Course, User, Cart


# get course information from database by id
def get_course_info(course_id):
    course_info = Course.get_course(id=course_id).first()
    if course_info is None:
        return jsonify({'message': 'Course not found!'}), 404
    return course_info

# count total price of all courses in cart


def count_total_price(user_id):
    cart_info = Cart.query.filter_by(user_id=user_id).all()
    total_price = 0
    for cart in cart_info:
        total_price += cart.total_price
    return total_price


# get user id by email
def get_user_id(email):
    if email is None:
        return jsonify({'message': 'User not found!'}), 404
    user_id = User.query.filter_by(email=email).first()
    if user_id is None:
        return jsonify({'message': 'User not found!'}), 404
    return user_id.id

from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies)
from website import db
from website.decorators.verify import token_required
from website.misc.HttpMethods import HttpMethods
from website.model import Cart
from website.views.cart.services import count_total_price, get_course_info

cart = Blueprint("cart", __name__)


# ------------------------------------------------------------------------------
# -----------------------------ROUTES-------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                       Add course to cart
# ------------------------------------------------------------------------------
@cart.route('/add-to-cart', methods=[HttpMethods.POST.value])
@jwt_required()
def add_course(userData):
    try:
        data = request.get_json()
        user_id = userData['id']
        course_id = data['course_id']
        quantity = data['quantity']
        cart_info = Cart.get_cart_by_user_id(user_id)
        course_in_cart = Cart.get_cart_by_id(course_id, user_id).first()
        course_price = get_course_info(course_id).course_price
        if course_in_cart:
            course_in_cart.quantity += quantity
            course_in_cart.total_price = course_in_cart.quantity*course_price
            db.session.commit()
            response = jsonify({"message": "Course added to cart"})
            response.status_code = 200
            return response

        total_price = quantity*course_price
        Cart.add_to_cart(user_id, course_id, quantity, total_price)

        response = jsonify(
            {"message": "Course added to cart", "count": len(cart_info)})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"message": "Error: "+str(e)})
        response.status_code = 500
        return response


# ------------------------------------------------------------------------------
#                       Get all courses in cart
# ------------------------------------------------------------------------------
@cart.route('/get-cart', methods=[HttpMethods.POST.value])
@token_required
def get_cart(userData):
    try:
        user_id = userData['id']
        cart_info = Cart.get_cart_by_user_id(user_id)
        if not cart_info:
            response = jsonify({"message": "Cart is empty"})
            response.status_code = 200
            return response
        courses = []
        price_total = 0
        for cart in cart_info:
            course = {}
            course['course_id'] = cart.course_id
            course['course_name'] = get_course_info(cart.course_id).course_name
            course['quantity'] = cart.quantity
            course['total_price'] = cart.total_price
            course['image'] = get_course_info(cart.course_id).course_image
            course['price'] = get_course_info(cart.course_id).course_price
            course['course_preview'] = get_course_info(
                cart.course_id).course_preview
            price_total += cart.total_price

            courses.append(course)
        response = jsonify({"message": "Cart is not empty", "courses": courses,
                           "total": price_total, 'count': len(cart_info)})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"message": "Error: "+str(e)})
        response.status_code = 500
        return response

# ------------------------------------------------------------------------------
#                     Check how many items are in the cart
# ------------------------------------------------------------------------------


@cart.route('/get-cart-count', methods=[HttpMethods.POST.value])
@token_required
def get_cart_count(data):
    try:
        if data['id'] is None:
            response = jsonify({"message": "Error: No user id"})
            response.status_code = 500
            return response
        user_id = data['id']
        cart_info = Cart.get_cart_by_user_id(user_id)
        if not cart_info:
            response = jsonify({"message": "Cart is empty", "count": 0})
            response.status_code = 200
            return response
        response = jsonify(
            {"message": "Cart is not empty", "count": len(cart_info)})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"message": "Error: "+str(e)})
        response.status_code = 500
        return response


# ------------------------------------------------------------------------------
#                     Remove course from user cart
# ------------------------------------------------------------------------------
@cart.route('/remove-from-cart', methods=[HttpMethods.POST.value])
@token_required
def remove_course(userData):
    try:
        data = request.get_json()
        course_in_cart = Cart.query.filter_by(
            userData['id'], data['course_id']).first()

        if course_in_cart:
            Cart.delete_from_cart(course_in_cart)
            response = jsonify({"message": "Course removed from cart"})
            response.status_code = 200
            return response

        response = jsonify({"message": "Course not in cart"})
        response.status_code = 500
        return response

    except Exception as e:
        response = jsonify({"message": "Error: "+str(e)})
        response.status_code = 500
        return response

# ------------------------------------------------------------------------------
#                     Total checkout price
# ------------------------------------------------------------------------------


@cart.route('/checkout', methods=[HttpMethods.POST.value])
@token_required
def checkout(userData):
    try:
        user_id = userData['id']
        cart_info = Cart.get_cart_by_user_id(user_id)
        if not cart_info:
            response = jsonify({"message": "Cart is empty", 'total': 0})
            response.status_code = 200
            return response
        price_total = count_total_price(user_id)
        response = jsonify(
            {"message": "Cart is not empty", "total": price_total})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"message": "Error: "+str(e)})
        response.status_code = 500
        return response

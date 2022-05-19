# import os
# import pathlib
# from functools import wraps
# from os import path

# from flask import Blueprint, current_app, request
# from flask.json import jsonify
# from jwt import decode
# from PIL import Image, ImageDraw, ImageFont
# from function_jwt import token_required

# from ..model import Course, User
# from website import db


# certif = Blueprint("certif", __name__)

# font = ImageFont.truetype('arial.ttf',150)
# font2 = ImageFont.truetype('arial.ttf',80)
# img = Image.open(pathlib.Path(__file__).parent.resolve()/'certificate.png')

# draw = ImageDraw.Draw(img)


# @certif.route('/certif', methods=['POST'])
# @token_required
# def certif_post(data):
#     print (data)
#     course_id = request.get_json()['course_id']
#     course = Course.query.filter_by(id=course_id).first()
#     course_category = course.course_category
#     author = User.query.filter_by(id=course.author).first()
#     author_name = author.username
#     name = data['name']
#     draw.text(xy=(300,600),text='{}'.format(name),fill=(255,255,255),font=font)
#     draw.text(xy=(200,1000),text='{}'.format(course_category),fill=(255,255,255),font=font2)
#     draw.text(xy=(1100,1000),text='{}'.format(author_name),fill=(255,255,255),font=font2)


#     img.save(pathlib.Path(__file__).parent.resolve()/'upload/certifications/{}.png'.format(name))

#     return jsonify({'message' : 'Certificate created!'}), 200

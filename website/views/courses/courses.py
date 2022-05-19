from os import path

from flask import Blueprint, current_app, request
from flask.json import jsonify
from website import db
from website.decorators.verify import token_required
from website.misc.courses import admin_check, course_object
from website.misc.HttpMethods import HttpMethods
from website.model import Course, Favorite, Lessons, Video
from website.views.courses.services import (get_length, get_lesson,
                                            get_video_by_id)

courses = Blueprint("courses", __name__)


# ------------------------------------------------------------------------------
# -----------------------------ROUTES-------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                       Add New courses  (You most be Admin)
# ------------------------------------------------------------------------------
@courses.route("/add_courses", methods=[HttpMethods.POST.value])
@token_required
def get_users(user):
    if admin_check(user):
        data = request.get_json()
        course_name = data['course_name']
        course = Course.check_course(course_name)
        if course:
            response = jsonify({"message": "Course already exists"})
            response.status_code = 400
            return response
        # add new course
        new_course = Course.add_courses(data)
        if new_course:
            response = jsonify({"message": "Course added successfully!"})
            response.status_code = 201
            return response
        else:
            response = jsonify({"message": "Error adding course!"})
            response.status_code = 400
            return response
    else:
        return jsonify({'message': 'You are not an admin!'})


# ------------------------------------------------------------------------------
#                       Get Courses
# ------------------------------------------------------------------------------
@courses.route("/get_courses", methods=[HttpMethods.GET.value])
def get_courses():
    try:
        courses = Course.get_courses()
        output = []
        for course in courses:
            course_data = course_object(course)
            output.append(course_data)
        return jsonify({'Courses': output})
    except Exception as e:
        return jsonify({'message': str(e)})


# ------------------------------------------------------------------------------
#                       Get Course By Id
# ------------------------------------------------------------------------------
@courses.route("/get_course/<id>", methods=[HttpMethods.POST.value])
def get_course( id):
    try :
        course = Course.get_course(id)
        # favourite = Favorite.get_favourites( id)
        lesson = get_lesson(id)
        course_data = course_object(course,  lesson)
        response = jsonify({'Course': course_data})
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'message': str(e)})


# -----------------------------------------------------------------------------------------------------------------------
#                       Add course to favourite or remove it from favourite if it is already there
# -----------------------------------------------------------------------------------------------------------------------
@courses.route("/add_to_favourite", methods=[HttpMethods.POST.value])
@token_required
def toggle_favourite(current_email):
    try:
        data = request.get_json()
        course_id = data['course_id']
        user_id = current_email['id']
        Favorite.toggle_favourite(user_id=user_id, course_id=course_id).first()
        response = jsonify({'message': 'Course has been updated!'})
        response.status_code = 200
        return response

    except:
        response = jsonify({'message': 'Course not found!'})
        response.status_code = 404
        return response


# ------------------------------------------------------------------------------
#                       Add Lesson to Course
# ------------------------------------------------------------------------------
@courses.route("/add_lesson", methods=[HttpMethods.POST.value])
def add_lesson():
    data = request.get_json()
    try:
        file = request.files['video']
        file.save(path.join(current_app.config['UPLOAD_VIDEO'], file.filename))

        new_lesson = Lessons.add_lesson(data)
        Video.add_video(lesson=new_lesson, video_name=file.filename, video_duration=get_length(
            path.join(current_app.config['UPLOAD_VIDEO'], file.filename)))
        db.commit()
        response = jsonify({'message': 'Lesson added successfully!'})
        response.status_code = 201
        return response
    except:
        response = jsonify({'message': 'Error adding lesson!'})
        response.status_code = 400
        return response


# ------------------------------------------------------------------------------
#                       get video by id
# ------------------------------------------------------------------------------
@courses.route("/show/<id>", methods=[HttpMethods.POST.value])
def show(id):
    vid = get_video_by_id(id)
    return vid

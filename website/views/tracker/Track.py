from flask import Blueprint, current_app, request
from flask.json import jsonify
from website import db
from website.decorators.verify import token_required
from website.misc.courses import (course_object, get_course, lessons_count,
                                  lessons_finished, lessons_not_finished)
from website.misc.HttpMethods import HttpMethods
from website.model import Course, Favorite, Lessons, User, Watchlist

Track = Blueprint("Track", __name__)


# ------------------------------------------------------------------------------
#                       Track Video WatchTime
# ------------------------------------------------------------------------------
@Track.route('/trackVideo', methods=[HttpMethods.POST.value])
@token_required
def trackVideo(userData):
    try:
        user_id = userData['id']
        data = request.get_json()
        lesson_id = data['lesson_id']
        course_id = data['course_id']
        watchTime = data['watchTime']
        finished = data['finished']
        lesson = Lessons.get_lesson(lesson_id)
        user = User.query.filter_by(id=user_id).first()
        if lesson is None:
            return jsonify({'message': 'Course not found!'}), 404
        if user is None:
            return jsonify({'message': 'User not found!'}), 404
        video = Watchlist.query.filter_by(
            lessons_id=lesson_id, user_id=user_id).first()
        if video is None:
            Watchlist.add_to_watchlist(
                lesson_id, user_id, watchTime, finished, course_id)
            response = jsonify({'message': 'Video added to watchlist!'})
            response.status_code = 201
            return response
        else:
            if video.finished == True:
                video.watchtime = watchTime
            else:
                video.watchtime = watchTime
                video.finished = finished
            db.session.commit()
            response = jsonify({'message': 'Video updated!'})
            response.status_code = 201
            return response
    except Exception as e:
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response


# ------------------------------------------------------------------------------
#                       Track Video Click
# ------------------------------------------------------------------------------
@Track.route('/trackClickVideo', methods=[HttpMethods.POST.value])
@token_required
def trackClickVideo(userData):
    user_id = userData['id']
    data = request.get_json()
    course_id = data['course_id']
    course = Course.get_course(id=course_id)
    user = User.query.filter_by(id=user_id).first()

    if course is None:
        response = jsonify({'message': 'Course not found!'})
        response.status_code = 404
        return response

    if user is None:
        response = jsonify({'message': 'User not found!'})
        response.status_code = 404
        return response

    click = Watchlist.track_click(course_id=course_id, user_id=user_id)
    if click:
        response = jsonify({"message": "Clicked!"})
        response.status_code = 201
        return response

    else:
        response = jsonify({"message": "Already Clicked!"})
        response.status_code = 201
        return response


# ------------------------------------------------------------------------------
#                       Remove Video Click
# ------------------------------------------------------------------------------
@Track.route('/deleteClick', methods=[HttpMethods.POST.value])
@token_required
def deleteClick(userData):
    try:
        user_id = userData['id']
        data = request.get_json()
        course_id = data['course_id']
        click = Watchlist.remove_click(course_id, user_id)
        if click is None:
            response = jsonify({'message': 'Click not found!'})
            response.status_code = 404
            return response
        else:
            response = jsonify({'message': 'Click removed!'})
            response.status_code = 201
            return response
    except Exception as e:
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response


# ------------------------------------------------------------------------------
#                       Get favourite course of the user
# ------------------------------------------------------------------------------
@Track.route("/get_favourite", methods=[HttpMethods.POST.value])
@token_required
def get_favourite(data):
    try:
        user_id = data['id']
        favourites = Favorite.query.filter_by(user_id=user_id).all()
        output = []
        for favourite in favourites:
            course = get_course(favourite.course_id)
            output.append(course_object(course))
        response = jsonify({'Favourites': output})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response


# ------------------------------------------------------------------------------
#                       Get completed course of the user
# ------------------------------------------------------------------------------
@Track.route("/get_completed", methods=[HttpMethods.POST.value])
@token_required
def get_completed(userData):
    try:
        user_id = userData['id']
        courses = Course.get_courses()
        output = []

        for course in courses:
            course_id = course.id
            finished = lessons_finished(course_id, user_id)
            lesson_count = lessons_count(course_id)
            if finished == lesson_count:
                course = get_course(course_id)
                output.append(course_object(course))
        response = jsonify({'Courses': output})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response


# ------------------------------------------------------------------------------
#                       Get watched course of the user
# ------------------------------------------------------------------------------
@Track.route("/get_watched", methods=[HttpMethods.POST.value])
@token_required
def get_watched(data):
    try:
        user_id = data['id']
        Watched = Watchlist.query.filter_by(
            user_id=user_id, finished=False).all()
        output = []
        for watched in Watched:
            course = get_course(watched.course_id)
            output.append(course_object(course))
        response = jsonify({'Watched': output})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response


# ------------------------------------------------------------------------------
#                       Get Lessons left course of the user
# ------------------------------------------------------------------------------
@Track.route("/get_lessons_left", methods=[HttpMethods.POST.value])
@token_required
def get_lessons_left(userData):
    try:
        user_id = userData['id']
        courses = Course.get_courses()
        output = []
        for course in courses:
            not_finished = lessons_not_finished(course.id, user_id)
            lesson_count = lessons_count(course.id)
            finished = lessons_finished(course.id, user_id)
            if not_finished > 0:
                course = get_course(course.id)
                course = course_object(course)
                course["total_lessons"] = lesson_count
                course["lessons_finished"] = finished
                output.append(course)
        response = jsonify({'Courses': output})
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response

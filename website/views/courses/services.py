import subprocess
from re import L

from flask import current_app, send_from_directory
from flask.json import jsonify
from website.model import Lessons, Video, Watchlist


# ------------------------------------------------------------------------------
#                       Get lessons of a course
# ------------------------------------------------------------------------------
def get_lesson(ids):
    lessons = Lessons.query.filter_by(course_id=ids).all()
    output = []
    column = ""
    lesson_name = []
    lesson_content = []
    lesson_duration = []
    lesson_lesson = []
    lesson_order = []
    lesson_id = []
    lesson_done = []
    lesson_data = {}
    lesson_data = {}
    column = ""
    id = 1
    i = 0
    for lesson in lessons:
        if not column:
            column = lesson.lesson_column
        i += 1
        if column == lesson.lesson_column:
            lesson_name.append(lesson.lesson_name)
            lesson_id.append(lesson.id)
            lesson_content.append(get_video_by_id(lesson.id))
            lesson_duration.append(get_video_duration(lesson.id))
            lesson_order.append(lesson.lesson_order)
            # lesson_done.append(check_lesson_done(lesson.id, user_id))
            lesson_lesson.append({"name": lesson.lesson_name, "id": lesson.id, "duration": get_video_duration(
                lesson.id), "order": lesson.lesson_order})
            if i == len(lessons):
                lesson_data['name'] = lesson_name
                lesson_data['duration'] = lesson_duration
                lesson_data['order'] = lesson_order
                lesson_data['lesson'] = lesson_lesson
                lesson_data['column'] = column
                lesson_data['id'] = lesson_id
                lesson_data['done'] = lesson_done
                output.append(lesson_data)
        else:
            lesson_data['name'] = lesson_name
            lesson_data['duration'] = lesson_duration
            lesson_data['order'] = lesson_order
            lesson_data['column'] = column
            lesson_data['lesson'] = lesson_lesson
            lesson_data['id'] = lesson_id
            lesson_data['done'] = lesson_done
            output.append(lesson_data)
            lesson_name = []
            lesson_content = []
            lesson_duration = []
            lesson_order = []
            lesson_lesson = []
            lesson_id = []
            lesson_done = []
            lesson_name.append(lesson.lesson_name)
            lesson_content.append(get_video_by_id(lesson.id))
            lesson_duration.append(get_video_duration(lesson.id))
            lesson_order.append(lesson.lesson_order)
            lesson_id.append(lesson.id)
            lesson_lesson.append({"name": lesson.lesson_name, "id": lesson.id, "duration": get_video_duration(
                lesson.id), "order": lesson.lesson_order})
            id += 1
            lesson_data = {}
            column = lesson.lesson_column
    return output


# ------------------------------------------------------------------------------
#                       Get video length
# ------------------------------------------------------------------------------
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)

# ------------------------------------------------------------------------------
#                       Get video By filename
# ------------------------------------------------------------------------------


def getVideo(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_VIDEO'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'message': 'No file found!'})


# ------------------------------------------------------------------------------
#                       Get video name By lesson id
# ------------------------------------------------------------------------------
def get_video_by_id(id):
    try:
        video = Video.query.filter_by(lesson=id).first()
        video = getVideo(video.video_name)
        return video
    except Exception as e:
        return jsonify({'message': 'No file found!'})


# ------------------------------------------------------------------------------
#                       Check if lesson is done
# ------------------------------------------------------------------------------
def check_lesson_done(lesson_id, user_id):
    done = Watchlist.query.filter_by(
        user_id=user_id, lessons_id=lesson_id).first()
    if done:
        if done.finished:
            return True
        else:
            return False
    else:
        return False

# ------------------------------------------------------------------------------
#                       Get video duration By lesson id
# ------------------------------------------------------------------------------


def get_video_duration(id):
    try:
        video = Video.query.filter_by(lesson=id).first()
        return video.video_duration
    except Exception as e:
        return jsonify({'message': 'No file found!'})

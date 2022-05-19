from website.model import Course, Favorite, Lessons, User, Watchlist

# ------------------------------------------------------------------------------
# -----------------------------METHODS------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                       Get course by id
# ------------------------------------------------------------------------------
def get_course(id):
    course = Course.query.filter_by(id=id).first()
    return course


# ------------------------------------------------------------------------------
#                       Check if The user is Admin
# ------------------------------------------------------------------------------
def admin_check(id):
    id = id['id']
    user = User.query.filter_by(id=id).first()
    admin = user.admin
    return admin


# ------------------------------------------------------------------------------
#                       Get The Author Name By User Id
# ------------------------------------------------------------------------------
def author_name(id):
    user = User.query.filter_by(id=id).first()
    name = user.username
    return name


# ------------------------------------------------------------------------------
#                       Get the author avatar
# ------------------------------------------------------------------------------
def author_avatar(id):
    user = User.query.filter_by(id=id).first()
    avatar = user.avatar
    return avatar


# ------------------------------------------------------------------------------
#                       Course Name to url
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                       Get course object
# ------------------------------------------------------------------------------
def course_object(course, favourite=None, lessons=None):
    course_data = {}
    course_data['course_id'] = course.id
    course_data['course_name'] = course.course_name
    course_data['course_image'] = course.course_image
    course_data['course_author'] = author_name(course.author)
    course_data['course_author_avatar'] = author_avatar(course.author)
    course_data['course_description'] = course.course_description
    course_data['course_preview'] = course.course_preview
    course_data['course_content'] = course.course_content
    course_data['course_price'] = course.course_price
    course_data['course_duration'] = course.course_duration
    course_data['course_category'] = course.course_category

    if favourite:
        course_data['favourite'] = favourite
    if lessons:
        course_data['lessons'] = lessons
    return course_data


# ------------------------------------------------------------------------------
#                       Get lessons count
# ------------------------------------------------------------------------------
def lessons_count(course_id):
    lessons = Lessons.query.filter_by(course_id=course_id).all()

    return len(lessons)


# ------------------------------------------------------------------------------
#                       Get lessons not finished
# ------------------------------------------------------------------------------
def lessons_not_finished(course_id, user_id):
    watchlist = Watchlist.query.filter_by(
        course_id=course_id, user_id=user_id, finished=False).all()
    count = len(watchlist)
    return count


# ------------------------------------------------------------------------------
#                       Get lessons finished
# ------------------------------------------------------------------------------
def lessons_finished(course_id, user_id):
    watchlist = Watchlist.query.filter_by(
        course_id=course_id, user_id=user_id, finished=True).all()
    count = len(watchlist)
    return count

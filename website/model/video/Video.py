from sqlalchemy.sql import func

from website import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson = db.Column(db.Integer, db.ForeignKey(
        'lessons.id', ondelete="CASCADE"), nullable=False)
    video_name = db.Column(db.String(150), nullable=False)
    video_duration = db.Column(db.Integer, nullable=False)

    def add_video(lesson, video_name, video_duration):
        video = Video(lesson=lesson, video_name=video_name,
                      video_duration=video_duration)
        db.session.add(video)
        return video

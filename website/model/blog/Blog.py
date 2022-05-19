from sqlalchemy.sql import func

from website import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.String, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

    def get_all():
        return Blog.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content
        db.session.commit()

    def search_id(self, id):
        return Blog.query.filter_by(id=id).first()

    def __repr__(self):
        return f"Blog('{self.title}', '{self.author}', '{self.content}')"

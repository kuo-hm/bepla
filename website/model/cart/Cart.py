from sqlalchemy.sql import func
from website import db


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Integer, nullable=True)

    def add_to_cart(user_id, course_id, quantity, total_price):
        cart = Cart(
            user_id=user_id,
            course_id=course_id,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(cart)
        db.session.commit()

    def get_cart_by_user_id(user_id):
        return Cart.query.filter_by(user_id=user_id).all()

    def get_cart_by_id(course_id, user_id):
        return Cart.query.filter_by(course_id=course_id, user_id=user_id).first()

    def delete_from_cart(cart):
        db.session.delete(cart)
        db.session.commit()

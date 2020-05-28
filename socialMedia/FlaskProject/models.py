from FlaskProject import bcrypt, login_manager, db
from flask_login import UserMixin, current_user
from flask import current_app
from datetime import datetime

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    passwd = db.Column(db.String(100), nullable=False)
    email= db.Column(db.String(40), nullable=False, unique=True)
    picture = db.Column(db.String(20), default="default-avatar.jpg")
    posts = db.relationship("Post", backref="author", lazy=True)

   

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

        

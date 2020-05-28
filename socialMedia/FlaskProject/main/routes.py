from flask import render_template, Blueprint
from FlaskProject.models import Post
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    posts = None
    if current_user.is_authenticated:
        posts = Post.query.order_by(Post.date.desc()).all()
    return render_template("home.html", title= "Home", posts=posts)
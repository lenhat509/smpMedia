from flask import render_template, request, redirect, flash, request, url_for, abort, Blueprint
from FlaskProject.posts.form import  PostForm
from FlaskProject.models import  Post, User
from flask_login import current_user, login_required
from FlaskProject import db
from datetime import datetime

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Create a post successfully!!')
        return redirect('/')
    return render_template('createPost.html', form=form)
@posts.route('/post/<int:post_id>', methods=['GET'])
@login_required
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', title='Post', post=post)
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if current_user.username != post.author.username:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date = datetime.now()
        db.session.commit()
        flash('Update post successfully!!')
        return redirect(f'/post/{post_id}')
    form.title.data = post.title
    form.content.data = post.content
    return render_template('createPost.html',title='Update Post' , form=form)
@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.username != post.author.username:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Delete post successfully!!')
    return redirect('/')

@posts.route('/author/<int:author_id>', methods=['GET'])
@login_required
def author(author_id):
    posts = User.query.order_by(Post.date.desc()).get(author_id).posts
    return render_template('home.html', posts = posts)
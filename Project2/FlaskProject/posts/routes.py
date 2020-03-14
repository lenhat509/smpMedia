from flask import render_template, request, redirect, flash, request, url_for, abort, Blueprint
from FlaskProject.posts.form import  PostForm
from FlaskProject.models import  Post
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        Post.createPost(form.title.data, form.content.data)
        flash('Create a post successfully!!')
        return redirect('/')
    return render_template('createPost.html', form=form)
@posts.route('/post/<int:post_id>', methods=['GET'])
@login_required
def post(post_id):
    post = Post.get_post(post_id) 
    return render_template('post.html', title='Post', post=post)
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.get_post(post_id)
    if current_user.get_name() != post[4]:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        Post.updatePost(form.title.data, form.content.data, post_id)
        flash('Update post successfully!!')
        return redirect(f'/post/{post_id}')
    form.title.data = post[1]
    form.content.data = post[2]
    return render_template('createPost.html',title='Update Post' , form=form)
@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.get_post(post_id)
    if current_user.get_name() != post[4]:
        abort(403)
    Post.detelePost(post_id)
    flash('Delete post successfully!!')
    return redirect('/')

@posts.route('/author/<int:author_id>', methods=['GET'])
@login_required
def author(author_id):
    posts = Post.get_user_posts(author_id)
    return render_template('home.html', posts = posts)
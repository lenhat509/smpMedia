from flask import render_template, request, redirect, flash, request, url_for, Blueprint, current_app
from FlaskProject.users.form import RegisterForm, LoginForm, UpdateForm, ResetPasswordForm, ResetRequestForm
from FlaskProject import mail
from FlaskProject.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from FlaskProject.users.utils import saveImage, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data, form.email.data)
        result = user.createUser()
        if result == True:
            flash(f'Account {form.username.data} is created successfully')
            return redirect('/login')
        else:
            form.username.errors.append("Username has already existed !")
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        result = user.checkUser()
        if result >0:
            flash('Login successfully!!')
            login_user(user, remember=False)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')
        elif result <0:
            form.username.errors.append('Username does not exists')
        else:
            form.password.errors.append('Wrong password')
    return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash('Logout successfully !!!')
    return redirect('/')


@users.route('/content', methods=['GET','POST'])
@login_required
def content():
    form = UpdateForm()
    if form.validate_on_submit():
        picture_name = current_user.get_image()
        if form.picture.data:
            picture_name =  saveImage(form.picture.data)
        result = current_user.updateUser(form.username.data, form.email.data, picture_name) 
        if result == True:
            flash("Update successfully !!")
        else:
            form.username.errors.append('Username already existed')
        return redirect('/content')
    form.username.data = current_user.get_name()
    form.email.data= current_user.get_email()
    return render_template('content.html', title='Profile', form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def send_request():
    if current_user.is_authenticated:
        return redirect('/')
    form = ResetRequestForm()
    if form.validate_on_submit():
        username = User.check_email(form.email.data)
        if username:
            send_reset_email(username, form.email.data)
            flash('The request has been sent. Please check your email')
        else:
            form.email.errors.append('Email does not exist in database')
    return render_template('reset_request.html', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect('/')
    name =  User.verify_token(token)
    if name is None:
        flash('Invalid token or token has expired')
        return redirect('/reset_password')
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            User.reset_user_password(name, form.password.data)
            flash('Reset password successfully !')
            return redirect('/login')
    return render_template('reset_password.html', form = form)
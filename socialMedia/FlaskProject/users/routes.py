from flask import render_template, request, redirect, flash, request, url_for, Blueprint, current_app
from FlaskProject.users.form import RegisterForm, LoginForm, UpdateForm, ResetPasswordForm, ResetRequestForm
from FlaskProject import mail, db, bcrypt
from FlaskProject.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from FlaskProject.users.utils import saveImage, send_reset_email, verify_token

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        data = User.query.filter_by(username=form.username.data).first()
        if data == None:
            hashpw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, passwd=hashpw, email=form.email.data)
            db.session.add(user)
            db.session.commit()
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
        data = User.query.filter_by(username=form.username.data).first()
        if data != None: 
            if bcrypt.check_password_hash(data.passwd, form.password.data):
                flash('Login successfully!!')
                login_user(data, remember=False)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('/')
            else:
                form.password.errors.append('Wrong password')
        else:
            form.username.errors.append('Username does not exists')
        
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
        data1 = User.query.filter_by(username=form.username.data).first()
        data2 = User.query.filter_by(email=form.email.data).first()
        if data1== None or data1.username == current_user.username  :
            if  data2== None or data2.email == current_user.email  :
                current_user.username = form.username.data
                current_user.email= form.email.data
                if form.picture.data:
                    picture_name =  saveImage(form.picture.data)
                    current_user.picture = picture_name
                db.session.commit()
                flash("Update successfully !!")
            else:
                form.email.errors.append('Username already existed')
        else:
            form.username.errors.append('Username already existed')
        return redirect('/content')
    form.username.data = current_user.username
    form.email.data= current_user.email
    return render_template('content.html', title='Profile', form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def send_request():
    if current_user.is_authenticated:
        return redirect('/')
    form = ResetRequestForm()
    if form.validate_on_submit():
        data = User.query.filter_by(email=form.email.data).first()
        if data:
            send_reset_email(data)
            flash('The request has been sent. Please check your email')
        else:
            form.email.errors.append('Email does not exist in database')
    return render_template('reset_request.html', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect('/')
    name =  verify_token(token)
    if name is None:
        flash('Invalid token or token has expired')
        return redirect('/reset_password')
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            data = User.query.filter_by(username=name).first()
            hashpw = bcrypt.generate_password_hash(form.password.data)
            data.passwd = hashpw
            db.session.commit()
            flash('Reset password successfully !')
            return redirect('/login')
    return render_template('reset_password.html', form = form)
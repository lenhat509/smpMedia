import os
import secrets
from flask import current_app, url_for
from FlaskProject import mail
from FlaskProject.models import User
from flask_mail import Message


def send_reset_email(name, email):
    token = User.get_token(name)
    msg = Message('Reset Your Password', sender='nonreply@mail.com', recipients=[email])
    msg.body = f'''Click the link to reset your password {url_for('users.reset_password', token = token, _external=True)}'''
    mail.send(msg)

def saveImage(file_field_data):
    random_name = secrets.token_hex(8)
    _ , ext = os.path.splitext(file_field_data.filename)
    Nfile_name = random_name + ext
    Npath = os.path.join(current_app.root_path, 'static', Nfile_name)
    file_field_data.save(Npath)
    return Nfile_name

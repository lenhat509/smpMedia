import os
import secrets
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from FlaskProject import mail
from FlaskProject.models import User
from flask_mail import Message


def send_reset_email(data):
    token = get_token(data.username)
    msg = Message('Reset Your Password', sender='nonreply@mail.com', recipients=[data.email])
    msg.body = f'''Click the link to reset your password {url_for('users.reset_password', token = token, _external=True)}'''
    mail.send(msg)

def saveImage(file_field_data):
    random_name = secrets.token_hex(8)
    _ , ext = os.path.splitext(file_field_data.filename)
    Nfile_name = random_name + ext
    Npath = os.path.join(current_app.root_path, 'static', Nfile_name)
    file_field_data.save(Npath)
    return Nfile_name

def get_token(username):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in = 600)
    return s.dumps({'username': username}).decode('utf-8')


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        return s.loads(token)['username']
    except:
        return None

    # def get_id(self):
    #     cur = mysql.connection.cursor()
    #     cur.execute(f"SELECT id FROM userInfo WHERE username = '{self.__username}'")
    #     result= cur.fetchall()
    #     mysql.connection.commit()
    #     cur.close()
    #     return result[0][0]
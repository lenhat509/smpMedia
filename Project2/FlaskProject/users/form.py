from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=6, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max= 16)])
    confirm= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email= StringField('Email', validators=[DataRequired(), Email()])
    submit= SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=6, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max= 16)])
    submit= SubmitField('Submit')
    remember= BooleanField('Remember')

class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=6, max=16)])
    email= StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpg'])])
    submit= SubmitField('Submit')

class ResetRequestForm(FlaskForm):
    email =StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Request')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max= 16)])
    confirm= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Reset Password')
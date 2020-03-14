from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = StringField('Content', validators=[DataRequired(), Length(min=10, max=1000)])
    submit= SubmitField('Submit')
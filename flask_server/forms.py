from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import EmailField, DateField, TimeField


class EventForm(FlaskForm):
    # this is the form for creating a new event
    # all the boxes correspond to a column in the 'Event' table
    title = StringField('Event Title (Required)', validators=[DataRequired()])
    event_date = DateField('Event Date (Required)', validators=[DataRequired()])
    event_time = TimeField('Event Time (Required)', validators=[DataRequired()])
    event_end_date = DateField('Event End Date (Optional)', validators=[Optional()])
    event_end_time = TimeField('Event End Time (Optional)', validators=[Optional()])
    content = TextAreaField('Event Description (Required)', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewsForm(FlaskForm):
    # this is the form for creating a new event
    # all the boxes correspond to a column in the 'Event' table
    title = StringField('News Headline (Required)', validators=[DataRequired()])
    start_date = DateField('Date Created (Optional)', validators=[Optional()])
    start_time = TimeField('Time Created (Optional)', validators=[Optional()])
    picture = FileField('Update Picture (Optional)', validators=[FileAllowed(['jpg', 'png']), Optional()])
    content = TextAreaField('Event Description (Required)', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmailForm(FlaskForm):
    email = EmailField('Enter Email Here:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    # will set a secure cookie to remember a login
    submit = SubmitField('Login')

class PresidentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Change President')

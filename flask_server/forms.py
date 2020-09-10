from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, TimeField
from wtforms.validators import DataRequired, Email, Optional
from wtforms.fields.html5 import EmailField


class EventForm(FlaskForm):
    # this is the form for creating a new post
    title = StringField('Event Title', validators=[DataRequired()])
    event_date = DateTimeField('Event Date & Start Time - Format = %Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    event_end = DateTimeField('Event End Date - Format = %Y-%m-%d %H:%M:%S - NOT Required', validators=[Optional()])
    content = TextAreaField('Event Description', validators=[DataRequired()])
    submit = SubmitField('Create Event')


class EmailForm(FlaskForm):
    email = EmailField('Enter Email Here:', validators=[DataRequired()])
    submit = SubmitField('Submit')
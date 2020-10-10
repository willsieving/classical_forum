from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import EmailField


class EventForm(FlaskForm):
    # this is the form for creating a new event
    # all the boxes correspond to a column in the 'Event' table
    title = StringField('Event Title', validators=[DataRequired()])
    event_date = DateTimeField('Event Date & Start Time - Format = %Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    event_end = DateTimeField('Event End Date - Format = %Y-%m-%d %H:%M:%S - NOT Required', validators=[Optional()])
    content = TextAreaField('Event Description', validators=[DataRequired()])
    submit = SubmitField('Create Event')


class NewsForm(FlaskForm):
    # this is the form for creating a new event
    # all the boxes correspond to a column in the 'Event' table
    title = StringField('News Headline (Required)', validators=[DataRequired()])
    news_date = DateTimeField('Manually set date and time posted - Format = %Y-%m-%d %H:%M:%S --- Default is time of posting (Optional)', validators=[Optional()])
    picture = FileField('Update Profile Picture (Optional)', validators=[FileAllowed(['jpg', 'png']), Optional()])
    content = TextAreaField('Event Description (Required)', validators=[DataRequired()])
    submit = SubmitField('Create Event')


class EmailForm(FlaskForm):
    email = EmailField('Enter Email Here:', validators=[DataRequired()])
    submit = SubmitField('Submit')


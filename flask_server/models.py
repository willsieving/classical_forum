from flask_server import db, login_manager
import datetime
# using datetime as a type of column
from flask_login import UserMixin
import pytz
timezone = pytz.timezone('America/Los_Angeles')

# this gets a user's ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Going to be using SQL Alchemy for database
# it is an OOM - object-oriented mapper
# allows us to access database like an object
# can use different databases in the same code (SQL lite, or another kind)

# Each class is a different table of the database

class User(db.Model, UserMixin):
    # usermixin is for user classes only and lets it inherit certain properties
    # inheriting will allow us to use different login extensions

    # each of these columns represents a data input from user registration

    id = db.Column(db.Integer, primary_key=True)
    # each user gets a unique ID to identify them
    username = db.Column(db.String(), unique=True, nullable=False)
    # everyone must have a username, and no one can have the same username as another (same with email)

    password = db.Column(db.String(), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)

    event_end = db.Column(db.DateTime)

    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.event_date.strftime('%m')
    # returns this when object printed i.e. print('object')


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    news_date = db.Column(db.DateTime, nullable=False, default=pytz.timezone('America/Los_Angeles').localize(datetime.datetime.now()))

    image_file = db.Column(db.String(20))

    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"News('{self.title}', '{self.news_date}')"

    # returns this when object printed i.e. print('object')


class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Email: {self.email}"

class President(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"President is {self.name}: {self.email}"


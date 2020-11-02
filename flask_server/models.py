from flask_server import db
import datetime
# using datetime as a type of column

# Going to be using SQL Alchemy for database
# it is an OOM - object-oriented mapper
# allows us to access database like an object
# can use different databases in the same code (SQL lite, or another kind)

# Each class is a different table of the database

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
    news_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    image_file = db.Column(db.String(20), default='news.png')

    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"News('{self.title}', '{self.news_date}')"

    # returns this when object printed i.e. print('object')


class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Email: {self.email}"


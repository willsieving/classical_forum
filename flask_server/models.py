from flask_server import db, login_manager
from flask import current_app
# can't import app object because we put it inside a function, have to use this flask thing
import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# for making tokens for using emails

# this gets a user's ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Going to be using SQL Alchemy for database
# it is an OOM - object-oriented mapper
# allows us to access database like an object
# can use different databases in the same code (SQL lite, or another kind)


class User(db.Model, UserMixin):
    # usermixin is for user classes only and lets it inherit certain properties
    # inheriting will allow us to use different login extensions

    # each of these columns represents a data input from user registration

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        # creates a token that expires in 1800 seconds (30 min)
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
        # returns the token object that has the id of the current user as the payload in utf-8 scrambled

    @staticmethod
    def verify_reset_token(token):
        # static method tells python that we don't need self as the first argument
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        # if the token is valid then it gets the user with the user_id inside the token

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        # this is what is returned when we print the object (i.e. print(object))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime(year=2020, month=12, day=28, hour=11, minute=12, second=42))

    event_end = db.Column(db.Time, default=datetime.time(hour=15, minute=12, second=53))

    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.event_date.strftime('%m')
    # returns this when object printed i.e. print('object')


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    news_date = db.Column(db.DateTime, nullable=False, default=datetime.date(2020, 12, 28))

    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    content = db.Column(db.Text, nullable=False, default='avatar_img.png')

    def __repr__(self):
        return f"News('{self.title}', '{self.news_date}')"

    # returns this when object printed i.e. print('object')



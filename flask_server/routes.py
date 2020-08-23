from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from flask_server import db
#from flask_server.posts.forms import PostForm
from flask_server.models import Event, News
from flask_login import current_user, login_required
import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    db.create_all()
    events = Event.query.order_by(Event.event_date.desc()).paginate(page=1, per_page=2)
    return render_template('home.html', events=events)

@main.route('/discussion')
def discussion():
    return render_template('discussion.html')

@main.route('/past_events')
def past_events():
    db.create_all()
    events = Event.query.order_by(Event.event_date.asc()).paginate(page=1, per_page=10)
    return render_template('past_events.html', events=events)

@main.route('/upcoming_events')
def upcoming_events():
    db.create_all()
    events = Event.query.order_by(Event.event_date.desc()).paginate(page=1, per_page=10)
    return render_template('upcoming_events.html', events=events)

@main.route('/news')
def news():
    db.create_all()
    news_db = News.query.order_by(News.news_date.desc()).paginate(page=1, per_page=10)
    return render_template('news.html', news=news_db)


@main.route('/event/new', methods=['GET', 'POST'])
def new_event():

    event = Event(title='July Test Event on the Fifteenth',
                  event_date=datetime.datetime(year=2020, month=7, day=15, hour=14, minute=12, second=0),
                  content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                  event_end=datetime.time(hour=16, minute=23, second=0))
    # here we are getting the post's data from the forms and putting it in out previously created Post() model
    db.session.add(event)
    # adding post to database
    db.session.commit()



    return redirect(url_for('main.home'))


@main.route('/news/new', methods=['GET', 'POST'])
def new_news():

    news = News(title='Test Event Title', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.')
    # here we are getting the post's data from the forms and putting it in out previously created Post() model
    db.session.add(news)
    # adding post to database
    db.session.commit()



    return redirect(url_for('main.home'))
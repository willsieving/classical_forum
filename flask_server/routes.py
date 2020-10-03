from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from flask_server import db
from flask_server.models import Event, News, Emails
from flask_server.forms import EventForm, EmailForm
import datetime

# Please don't judge my sloppy code, tried to comment as best I could.


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    db.create_all()
    # Creating database in case there isn't already one
    events = Event.query.order_by(Event.event_date.desc()).paginate(page=1, per_page=2)
    # Query first two rows of event table in descending order
    current_datetime = datetime.datetime.utcnow()
    # Store current date in datetime obj

    form = EmailForm()
    # form obj for emails

    if form.validate_on_submit():
        #
        email = Emails(email=form.email.data)
        # here we are getting the data from the form and putting it in the email table of the database
        db.session.add(email)
        # adding email to database
        db.session.commit()
        flash('Your event has been created!', 'success')
        # flashing not set up yet
        return redirect(url_for('main.home'))

    return render_template('home.html', events=events, current_datetime=current_datetime, form=form)


@main.route('/discussion')
def discussion():
    return render_template('discussion.html')


@main.route('/past_events', methods=['GET', 'POST'])
def past_events():
    db.create_all()
    # redundant database creation
    events = Event.query.order_by(Event.event_date.asc())
    # query all events
    page = request.args.get('page', default=1, type=int)
    # set page

    month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    month_names = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
                   '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
    # list and dictionary for listing out the months and only showing the events for the given month

    current_year = datetime.datetime.today().strftime('%Y')
    # storing current year in a variable

    year_list = range(2017, int(current_year))
    # make the sure the list of years can increase as current year increases

    current_datetime = datetime.datetime.utcnow()
    # current datetime

    # ignore below, testing
    print('here', request.method)
    if request.method == 'POST':
        if 'submit_button' in request.form:
            user_answer = request.form['event_year']
            return user_answer

    # once the inputs work this variable will be what the user selects on the year selection
    year_selected = '2020'

    # pass all the objs and variables into the html page
    return render_template('past_events.html', events=events, current_datetime=current_datetime,
                           page=page, month_list=month_list, month_names=month_names,
                           year_list=reversed(year_list), current_year=int(current_year), year_selected=year_selected)


@main.route('/event/<int:event_id>')
# you can use a variable within the route name (here is will create a page for each post id)
# you can specify whether the variable should should be an integer, string, etc, with 'int:' or 'string:'
def event(event_id):
    # have to pass in the variable in the definition
    event_query = Event.query.get_or_404(event_id)
    # get me the post with the ID of post_id (if none exists return a 404)
    return render_template('event.html', title=event_query.title, event=event_query)


# testing trying to get posting to work
@main.route('/past_events', methods=['POST'])
def year_post():
    year = request.form.getlist('event_year')
    print(year)


# TO DO
@main.route('/upcoming_events')
def upcoming_events():
    db.create_all()
    events = Event.query.order_by(Event.event_date.desc()).paginate(page=1, per_page=10)
    return render_template('upcoming_events.html', events=events)


# TO DO
@main.route('/news')
def news():
    db.create_all()
    news_db = News.query.order_by(News.news_date.desc()).paginate(page=1, per_page=10)
    return render_template('news.html', news=news_db)


# TO DO
@main.route('/contact')
def contact():
    return render_template('contact.html')


# Gets the data from the forms and and posts it to database
@main.route('/event/new', methods=['GET', 'POST'])
def new_event():

    form = EventForm()

    if form.validate_on_submit():
        event = Event(title=form.title.data,
                      event_date=form.event_date.data,
                      content=form.content.data,
                      event_end=form.event_end.data)
        # here we are getting the data from the forms and putting it in the database
        db.session.add(event)
        # adding event to database
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('new_event.html', title='New Event',
                           form=form, legend='New Event')


# Creates new row in the News tables of database
# TO DO: Write HTML
@main.route('/news/new', methods=['GET', 'POST'])
def new_news():

    news = News(title='Test Event Title', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.')

    db.session.add(news)
    db.session.commit()

    return redirect(url_for('main.home'))
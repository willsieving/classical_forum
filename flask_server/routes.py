from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from flask_server import db
from flask_server.models import Event, News, Emails
from flask_server.forms import EventForm, EmailForm, NewsForm
import datetime

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import secrets
import os
from PIL import Image
# ^ helps us resize uploaded photos
from flask import url_for, current_app
# current app grabs the current app in use that is now hidden in a function in __init__


# Please don't judge my sloppy code, tried to comment as best I could.




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # use _ for unused variables (in this case the file's name)
    # because the input of the form is a file,
    # it has a filename attribute that can be split into the name and the extension
    # (we want to keep the extension and rename the file with a random hex, adding the extension)

    image_data = request.FILES[form_picture.name].read()

    #### IDK WHAT TO DO

    picture_fn = random_hex + '.jpg'
    # creating picture name (random 8 digit hex + the extension)

    picture_path = os.path.join(current_app.root_path, 'static/news_pictures/', picture_fn)
    # creating the path into which the picture will be saved
    # (i.e. root path of app + static/profile_pics/picture_name+extension)
    output_size = (150, 150)
    # here we set the size output for the resizer
    i = Image.open(image_data)
    # opening the inputted picture into the i variable
    i = i.resize(size=output_size)
    # reducing the size of i with output_size
    i.save(picture_path)
    # saving the newly resized picture to the created path
    # no longer saves the large version of the image
    return picture_fn
    # returns the picture name


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    db.create_all()
    # Creating database in case there isn't already one
    current_datetime = datetime.datetime.utcnow()
    events = Event.query.order_by(Event.event_date.asc()).filter(Event.event_date >= current_datetime).paginate(page=1)

    news_query = News.query.order_by(News.news_date.desc()).paginate(page=1, per_page=2)
    # Query first two rows of event table in descending order

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

    return render_template('home.html', events=events, news=news_query, current_datetime=current_datetime, form=form)


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

    if request.method == 'POST':
        year_selected = int(request.form['event_year'])
        str_year_sel = request.form['event_year']
    else:
        year_selected = 2020
        str_year_sel = '2020'

    # once the inputs work this variable will be what the user selects on the year selection


    # pass all the objs and variables into the html page
    return render_template('past_events.html', events=events, current_datetime=current_datetime,
                           page=page, month_list=month_list, month_names=month_names, str_year_sel=str_year_sel,
                           year_list=reversed(year_list), current_year=int(current_year), year_selected=year_selected,
                           title='Past Events')


@main.route('/event/<int:event_id>')
# you can use a variable within the route name (here is will create a page for each post id)
# you can specify whether the variable should should be an integer, string, etc, with 'int:' or 'string:'
def event(event_id):
    # have to pass in the variable in the definition
    event_query = Event.query.get_or_404(event_id)
    # get me the post with the ID of post_id (if none exists return a 404)
    return render_template('event.html', title=event_query.title, event=event_query)


@main.route('/news/<int:news_id>')
# you can use a variable within the route name (here is will create a page for each post id)
# you can specify whether the variable should should be an integer, string, etc, with 'int:' or 'string:'
def news_item(news_id):
    # have to pass in the variable in the definition
    news_query = News.query.get_or_404(news_id)
    # get me the post with the ID of post_id (if none exists return a 404)
    return render_template('news_item.html', title=news_query.title, news=news_query)


# TO DO
@main.route('/upcoming_events')
def upcoming_events():
    db.create_all()
    current_datetime = datetime.datetime.utcnow()
    events = Event.query.order_by(Event.event_date.asc()).filter(Event.event_date >= current_datetime).paginate(page=1)
    return render_template('upcoming_events.html', events=events, title='Upcoming Events')


# TO DO
@main.route('/news', methods=['GET', 'POST'])
def news():
    db.create_all()
    news_db = News.query.order_by(News.news_date.desc()).paginate(page=1)

    current_year = datetime.datetime.today().strftime('%Y')
    # storing current year in a variable

    year_list = list(range(2017, int(current_year)))
    # make the sure the list of years can increase as current year increases
    year_list.reverse()

    if request.method == 'POST':
        year_selected = int(request.form['news_year'])
        str_year_sel = request.form['news_year']
    else:
        year_selected = 2020
        str_year_sel = '2020'

    current_datetime = datetime.datetime.utcnow()

    return render_template('news.html', news=news_db, current_year=current_year, year_list=year_list,
                           current_datetime=current_datetime, year_selected=year_selected, str_year_sel=str_year_sel,
                           title='News')


# TO DO
@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


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

@main.route('/event/<int:event_id>/update', methods=['GET', 'POST'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm()
    if form.validate_on_submit():
        event_date_obj = datetime.datetime.strptime(str(form.event_date.data), '%Y-%m-%d %H:%M:%S')
        event_end_obj = datetime.datetime.strptime(str(form.event_end.data), '%Y-%m-%d %H:%M:%S')
        event.title = form.title.data
        event.content = form.content.data
        event.event_date = event_date_obj
        event.event_end = event_end_obj
        # here we set the value of things already in the database, so we don't need a db.session.add
        # only to commit the changes
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.event', event_id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        # fill in the form with the content of the post (so it can be edited)
        # if the request is a get request which it should always be
        form.content.data = event.content
        form.event_date.data = event.event_date
        form.event_end.data = event.event_end

    return render_template('new_event.html', title='Update Event',
                           form=form, legend='Update Event')


@main.route('/event/<int:event_id>/delete', methods=['POST', 'GET'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    db.session.delete(event)
    # deleting the post from the database
    db.session.commit()
    # committing the changes
    flash('Your post has been deleted!', 'success')
    # flashing a success message
    return redirect(url_for('main.home'))
    # redirecting to the home page


@main.route('/news/<int:news_id>/update', methods=['GET', 'POST'])
def update_news(news_id):
    news = News.query.get_or_404(news_id)
    form = NewsForm()
    if form.validate_on_submit():
        news_date_obj = datetime.datetime.strptime(str(form.start_date.data) + ' ' + str(form.start_time.date), '%Y-%m-%d %H:%M:%S')
        news.title = form.title.data
        news.content = form.content.data
        news.news_date = news_date_obj
        # here we set the value of things already in the database, so we don't need a db.session.add
        # only to commit the changes
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.news_item', news_id=news.id))
    elif request.method == 'GET':
        form.title.data = news.title
        # fill in the form with the content of the post (so it can be edited)
        # if the request is a get request which it should always be
        form.content.data = news.content
        form.start_date.data = news.news_date
        form.start_time.data = news.news_date

    return render_template('new_news.html', title='Update News',
                           form=form, legend='Update News')


@main.route('/news/<int:news_id>/delete', methods=['POST', 'GET'])
def delete_news(news_id):
    news = News.query.get_or_404(news_id)

    db.session.delete(news)
    # deleting the post from the database
    db.session.commit()
    # committing the changes
    flash('Your post has been deleted!', 'success')
    # flashing a success message
    return redirect(url_for('main.home'))
    # redirecting to the home page


# Gets the data from the forms and and posts it to database
@main.route('/news/new', methods=['GET', 'POST'])
def new_news():

    form = NewsForm()

    if form.validate_on_submit():
        image_dir = os.path.join(os.getcwd(), "flask_server\\static\\news_pictures")
        if form.picture.data:
            random_hex = secrets.token_hex(8)
            picture_file = form.picture.data
            _, f_ext = os.path.splitext(picture_file.filename)
            picture_fn = random_hex + f_ext

            pic_filename = secure_filename(picture_fn)

            # Document and Profile photo save
            # picture_file.save(os.path.join(image_dir, pic_filename))

            output_size_thumbnail = [75, 75]
            output_size_page = [400, 400]
            i = Image.open(picture_file)
            i2 = i.resize(output_size_thumbnail)
            i3 = i.resize(output_size_page)
            i2.save(os.path.join(image_dir, pic_filename))
            i3.save(os.path.join(image_dir, '1'+pic_filename))
        else:
            pic_filename = None
        if form.start_date.data and form.start_time.data:
            news_date_entry = datetime.datetime.strptime(str(form.start_date.data) + ' ' + str(form.start_time.data), "%Y-%m-%d %H:%M:%S")
        else:
            news_date_entry = None

        new_news = News(title=form.title.data,
                        content=form.content.data,
                        news_date=news_date_entry,
                        image_file=pic_filename)

        # here we are getting the data from the forms and putting it in the database
        db.session.add(new_news)
        # adding event to database
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('new_news.html', title='New News',
                           form=form, legend='New News')
from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from flask_server import db, bcrypt
from flask_server.models import Event, News, Emails, User, President
from flask_server.forms import EventForm, EmailForm, NewsForm, LoginForm, PresidentForm
from flask_login import login_user, current_user, logout_user, login_required
import datetime

from sqlalchemy import func

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import secrets
import os
from PIL import Image
# ^ helps us resize uploaded photos
from flask import url_for, current_app
# current app grabs the current app in use that is now hidden in a function in __init__
import pytz
timezone = pytz.timezone('America/Los_Angeles')

# Please don't judge my sloppy code, tried to comment as best I could.


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():

    db.create_all()
    # Creating database in case there isn't already one
    current_datetime = datetime.datetime.utcnow()
    events = Event.query.order_by(Event.event_date.asc()).filter(Event.event_date >= current_datetime).paginate(page=1)

    news_query = News.query.order_by(News.news_date.desc()).paginate(page=1, per_page=3)
    # Query first two rows of event table in descending order
    list_news_id = []
    for item in news_query.items:
        if item.image_file:
            list_news_id.append(item.id)

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

    return render_template('home.html', list_news_id=list_news_id, events=events, news=news_query, current_datetime=current_datetime, form=form, current_user=current_user)

@main.route('/create_president')
def create_president():
    president = President(name="Test Name", email="test@email.com")
    # here we are getting the data from the form and putting it in the email table of the database
    db.session.add(president)
    # adding email to database
    db.session.commit()
    return redirect(url_for('main.admin'))

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

    qry = db.session.query(func.min(Event.event_date).label("min_score"))
    # Grab oldest event for year selection
    qry2 = db.session.query(func.max(Event.event_date).label("max_score"))
    # Grab max
    res = qry.one()
    res2 = qry2.one()
    min = res.min_score
    max = res2.max_score

    qry3 = Event.query.order_by(Event.event_date.desc())
    yr_include = []
    current_datetime = datetime.datetime.now()

    for item in qry3:
        datetime_item = pytz.timezone('America/Los_Angeles').localize(item.event_date)
        datetime_current = pytz.timezone('America/Los_Angeles').localize(current_datetime)
        if datetime_item <= datetime_current:
            yr_include.append(int(item.event_date.strftime('%Y')))
    if min:
        earlier_year = int(min.strftime('%Y'))
    else:
        earlier_year = int(datetime.datetime.now().strftime('%Y'))

    if max:
        max_year = int(max.strftime('%Y'))
    else:
        max_year = int(datetime.datetime.now().strftime('%Y'))

    if max_year != earlier_year:
        year_list = list(range(earlier_year, max_year))
        year_list.append(int(max_year))
    else:
        year_list = [earlier_year]

    # make the sure the list of years can increase as current year increases


    # current datetime

    if request.method == 'POST':
        year_selected = int(request.form['event_year'])
        str_year_sel = request.form['event_year']
    else:
        if max_year != earlier_year:
            if max_year not in yr_include:
                year_selected = int(max_year)
                while year_selected > int(yr_include[0]):
                    year_selected = year_selected - 1
                str_year_sel = str(year_selected)
            else:
                year_selected = int(max_year)
                while year_selected > int(current_year):
                    year_selected = year_selected - 1
                str_year_sel = str(year_selected)
        else:
            year_selected = int(earlier_year)
            str_year_sel = str(earlier_year)
    # once the inputs work this variable will be what the user selects on the year selection
    print(year_selected, str_year_sel)
    yr_include = set(yr_include)
    yr_include = list(yr_include)
    yr_include.reverse()
    # pass all the objs and variables into the html page
    return render_template('past_events.html', events=events, current_datetime=current_datetime,
                           page=page, month_list=month_list, month_names=month_names, str_year_sel=str_year_sel,
                           year_list=reversed(year_list), current_year=int(current_year), year_selected=year_selected,
                           title='Past Events', yr_include=yr_include)


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

    current_year = datetime.datetime.now(timezone).strftime('%Y')
    # storing current year in a variable

    qry = db.session.query(func.min(News.news_date).label("min_score"))
    # Grab oldest event for year selection
    qry2 = db.session.query(func.max(News.news_date).label("max_score"))
    # Grab max
    qry3 = News.query.order_by(News.news_date.desc())
    yr_include = []

    current_datetime = datetime.datetime.now()


    for item in qry3:
        datetime_item = pytz.timezone('America/Los_Angeles').localize(item.news_date)
        datetime_current = pytz.timezone('America/Los_Angeles').localize(current_datetime)
        if datetime_item <= datetime_current:
            yr_include.append(int(item.news_date.strftime('%Y')))

    res = qry.one()
    res2 = qry2.one()
    min = res.min_score
    max = res2.max_score

    if min:
        earlier_year = int(min.strftime('%Y'))
    else:
        earlier_year = int(datetime.datetime.now(timezone).strftime('%Y'))

    if max:
        max_year = int(max.strftime('%Y'))
    else:
        max_year = int(datetime.datetime.now(timezone).strftime('%Y'))

    if max_year != earlier_year:
        year_list = list(range(earlier_year, max_year))
        year_list.append(int(max_year))
    else:
        year_list = [earlier_year]
    # make the sure the list of years can increase as current year increases
    year_list.reverse()
    if request.method == 'POST':
        year_selected = int(request.form['news_year'])
        str_year_sel = request.form['news_year']
    else:
        if max_year != earlier_year:
            if max_year not in yr_include:
                year_selected = int(max_year)
                while year_selected > int(yr_include[0]):
                    year_selected = year_selected - 1
                str_year_sel = str(year_selected)
            else:
                year_selected = int(max_year)
                while year_selected > int(current_year):
                    year_selected = year_selected - 1
                str_year_sel = str(year_selected)
        else:
            year_selected = int(earlier_year)
            str_year_sel = str(earlier_year)
        # once the inputs work this variable will be what the user selects on the year selection
    yr_include = set(yr_include)
    yr_include = list(yr_include)
    yr_include.reverse()
    return render_template('news.html', news=news_db, current_year=current_year, year_list=year_list,
                           current_datetime=current_datetime, year_selected=year_selected, str_year_sel=str_year_sel,
                           title='News', yr_include=yr_include)


# TO DO
@main.route('/contact')
def contact():
    president = President.query.all()
    return render_template('contact.html', title='Contact', president=president)

@main.route('/admin')
@login_required
def admin():


    return render_template('admin.html', title='Admin')

@main.route('/emails')
@login_required
def emails():
    emails = Emails.query.all()
    return render_template('emails.html', emails=emails, title='Emails')


# Gets the data from the forms and and posts it to database
@main.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():

    form = EventForm()

    if form.validate_on_submit():
        if form.event_date.data and form.event_time.data:
            event_date_entry = pytz.timezone('America/Los_Angeles').localize(datetime.datetime.strptime(str(form.event_date.data) + ' ' + str(form.event_time.data), "%Y-%m-%d %H:%M:%S"))
        else:
            event_date_entry = None
        if form.event_end_date.data and form.event_end_time.data:
            event_end_entry = pytz.timezone('America/Los_Angeles').localize(datetime.datetime.strptime(str(form.event_end_date.data) + ' ' + str(form.event_end_time.data), "%Y-%m-%d %H:%M:%S"))
        else:
            event_end_entry = None
        print(event_end_entry, event_date_entry.tzinfo, event_date_entry)
        event = Event(title=form.title.data,
                      event_date=event_date_entry,
                      content=form.content.data,
                      event_end=event_end_entry)
        # here we are getting the data from the forms and putting it in the database
        db.session.add(event)
        # adding event to database
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('new_event.html', title='New Event',
                           form=form, legend='New Event')

@main.route('/event/<int:event_id>/update', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm()
    if form.validate_on_submit():
        event_date_obj = datetime.datetime.strptime(str(form.event_date.data) + ' ' + str(form.event_time.data),
                                                   '%Y-%m-%d %H:%M:%S')
        if form.event_end_date.data and form.event_end_time.data:
            event_end_date_obj = datetime.datetime.strptime(str(form.event_end_date.data) + ' ' + str(form.event_end_time.data),
                                                    '%Y-%m-%d %H:%M:%S')
            event.event_end = event_end_date_obj

        event.title = form.title.data
        event.content = form.content.data
        event.event_date = event_date_obj

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
        form.event_time.data = event.event_date
        form.event_end_date.data = event.event_end
        form.event_end_time.data = event.event_end

    return render_template('new_event.html', title='Update Event',
                           form=form, legend='Update Event')


@main.route('/event/<int:event_id>/delete', methods=['POST', 'GET'])
@login_required
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
@login_required
def update_news(news_id):
    news = News.query.get_or_404(news_id)
    form = NewsForm()
    if form.validate_on_submit():
        if form.start_date.data and form.start_time.data:
            news_date_obj = datetime.datetime.strptime(str(form.start_date.data) + ' ' + str(form.start_time.data), '%Y-%m-%d %H:%M:%S')
            news.news_date = news_date_obj
        news.title = form.title.data
        news.content = form.content.data

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
@login_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)
    filename = news.image_file
    db.session.delete(news)
    # deleting the post from the database
    db.session.commit()
    # committing the changes
    cwd = os.getcwd()
    path_to_file = f'{cwd}/flask_server/static/news_pictures/{filename}'
    path_to_file2 = f'{cwd}/flask_server/static/news_pictures/carousel{filename}'
    if os.path.exists(path_to_file):
        os.remove(path_to_file)
    if os.path.exists(path_to_file2):
        os.remove(path_to_file2)
    flash('Your post has been deleted!', 'success')
    # flashing a success message
    return redirect(url_for('main.news'))
    # redirecting to the home page


# Gets the data from the forms and and posts it to database
@main.route('/news/new', methods=['GET', 'POST'])
@login_required
def new_news():

    form = NewsForm()

    def crop_to_aspect(image, aspect, divisor=1, alignx=0.5, aligny=0.5):
        """Crops an image to a given aspect ratio.
        Args:
            aspect (float): The desired aspect ratio.
            divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
            alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
            aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
        Returns:
            Image: The cropped Image object.
        """
        if image.width / image.height > aspect / divisor:
            newwidth = int(image.height * (aspect / divisor))
            newheight = image.height
        else:
            newwidth = image.width
            newheight = int(image.width / (aspect / divisor))
        img = image.crop((alignx * (image.width - newwidth),
                         aligny * (image.height - newheight),
                         alignx * (image.width - newwidth) + newwidth,
                         aligny * (image.height - newheight) + newheight))
        return img

    if form.validate_on_submit():
        # NOTE: If server is hosted on Linux, the path must use forward slashes rather than double back slashes
        image_dir = os.path.join(os.getcwd(), "flask_server/static/news_pictures")
        if form.picture.data:
            random_hex = secrets.token_hex(8)
            picture_file = form.picture.data
            _, f_ext = os.path.splitext(picture_file.filename)
            picture_fn = random_hex + f_ext

            pic_filename = secure_filename(picture_fn)

            # Document and Profile photo save
            # picture_file.save(os.path.join(image_dir, pic_filename))

            i = Image.open(picture_file)
            width, height = i.size  # Get dimensions
            output_size_page = [width, height]
            i2 = crop_to_aspect(i, 1)
            i3 = i.resize(output_size_page)
            i3.save(os.path.join(image_dir, pic_filename))
            i2.save(os.path.join(image_dir, ('carousel' + pic_filename)))
        else:
            pic_filename = None
        if form.start_date.data and form.start_time.data:
            news_date_entry = datetime.datetime.strptime(str(form.start_date.data) + ' ' + str(form.start_time.data), "%Y-%m-%d %H:%M:%S")
        else:
            news_date_entry = datetime.datetime.now()

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


@main.route('/register', methods=['GET', 'POST'])
# methods allows us to accept post requests such as the submit one
def register():

    #if the user is already logged in it will redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    hashed_password = bcrypt.generate_password_hash('2$`CT6[aXMVg~v{)').decode('utf-8')

    user = User(username='admin', password=hashed_password)
    president = President(name='Test Name', email='test@email.com')
    # This is fake login info, and it will be changed once the website is running!!!

    db.session.add(user)
    db.session.add(president)
    db.session.commit()
    flash(f'Your account has been created! You are now able to log in.', 'success')
    # if the form was valid on submit then flash this string
    # flash messages are only one time, and disappear on reload
    return redirect(url_for('main.login'))
    # this redirects the user to the login page if the form submit is a success
    # url_for just grabs the url of a given class/route name (home() in this case)


@main.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in it will redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # will check if there are any emails that same as the one entered
        # and will return first one found (there should only be one)

        if user and bcrypt.check_password_hash(user.password, form.password.data):
        # this will check if the user's password equal the un-hashed one entered on register
        # (hashed password was stored on database)
        # use check password hash to see if it works

            login_user(user, remember=form.remember.data)
            # this will log the user in

            next_page = request.args.get('next')
            # will get the next page that user wanted access but was redirected to login
            return redirect(next_page) if next_page else redirect(url_for('main.admin'))
            # this will redirect to the page that user wanted to go to before they logged in
            # otherwise goes to home
        else:
            # if login is successful then flash this message
            flash('Login Unsuccessful. Please check email and password.', 'danger')
        # if login failed then flash danger message and don't redirect
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/email/<int:email_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_email(email_id):
    emails = Emails.query.get_or_404(email_id)

    db.session.delete(emails)
    # deleting the post from the database
    db.session.commit()
    # committing the changes
    flash('Your post has been deleted!', 'success')
    # flashing a success message
    return redirect(url_for('main.emails'))
    # redirecting to the home page

@main.route('/president/<int:president_id>/delete', methods=['GET', 'POST'])
@login_required
def president_delete(president_id):
    president = President.query.get_or_404(president_id)
    db.session.delete(president)
    db.session.commit()

    return redirect(url_for('main.contact'))

@main.route('/president/<int:president_id>/update', methods=['GET', 'POST'])
@login_required
def president(president_id):
    president = President.query.get_or_404(president_id)
    form = PresidentForm()
    if form.validate_on_submit():
        president.name = form.name.data
        president.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.contact'))
    elif request.method == 'GET':
        form.name.data = president.name
        # fill in the form with the content of the post (so it can be edited)
        # if the request is a get request which it should always be
        form.email.data = president.email

    return render_template('president.html', title='Update President',
                           form=form, legend='Update President')


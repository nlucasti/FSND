#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.sql.functions import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy=True, passive_deletes=True)

    def get_venue(self):
        data = {
        "id":self.id,
        "name":self.name,
        "shows":self.shows
        }
        return(data)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), nullable = False, default = False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist', lazy=True, passive_deletes=True)


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key = True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete="CASCADE"), nullable = False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete="CASCADE"), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    venues = db.relationship('Venue', backref='Show', lazy=True)
#db.create_all()
#run flask db Migrate
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value.strftime("%m/%d/%Y, %H:%M:%S"))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  areas = Venue.query.distinct('city','state').all()
  data = []
  for area in areas:
      venues = Venue.query.filter(Venue.city == area.city, Venue.state == area.state).all()
      counts = venues
      record = {
        'city': area.city,
        'state': area.state,
        'venues': [venue.get_venue() for venue in venues],
      }
      data.append(record)


  return render_template('pages/venues.html',areas=data);# areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  venues = Venue.query.filter(Venue.name.ilike('%'+request.form.get('search_term', '')+'%')).all()
  count_shows = []
  count = 0
  venue_count = 0
  for venue in venues:
      for show in venue.shows:
          if show.start_time > datetime.now():
              count += 1
      count_shows.append(count)
      venue_count+=1
  response={ "count": venue_count}
  record= []

  for venue, count_iter in zip(venues, count_shows):
      venue_dict = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": count_iter
        }
      record.append(venue_dict)
  response['data'] = record
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.filter_by(id=venue_id).all()
  venue = venue[0]
  shows = db.session.query(Show.venue_id.label('venue_id'), (Artist.name).label('artist_name'), (Artist.image_link).label('artist_image_link'),Show.start_time).filter_by(venue_id=venue_id).join(Artist).all()
  past_shows = []
  upcoming_shows = []
  for show in shows:
      if show.start_time < datetime.now():
          past_shows.append(show)
      else:
          upcoming_shows.append(show)
  print(past_shows)
  data = {
    "id": venue.id,
    "name": venue.name,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,#[show[0] for show in venue.shows],
    "upcoming_shows": upcoming_shows,#[show[0] for show in venue.shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
 try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website = request.form['website']
      seeking_talent = request.form['seeking_talent'] == 'True'
      seeking_description = request.form['seeking_description']

      venue = Venue(name = name, city = city, state=state,
                    phone=phone, address=address, image_link=image_link, facebook_link=facebook_link, website = website,
                    seeking_talent=seeking_talent, seeking_description=seeking_description)
    # on successful db insert, flash success
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
 except:
     db.session.rollback()
     flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
 finally:
      db.session.close()

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
 return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
 try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue was successfully deleted.')
 except:
     db.session.rollback()
     flash('An error occurred. Venue could not be deleted.')
 finally:
      db.session.close()

 return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = []
    for artist in artists:
        record = {
          'id': artist.id,
          'name': artist.name
        }
        data.append(record)
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artists = Artist.query.filter(Artist.name.ilike('%'+request.form.get('search_term', '')+'%')).all()
  count_shows = []
  count =0
  artist_count = 0
  for artist in artists:
      for show in artist.shows:
          if show.start_time > datetime.now():
              count += 1
      count_shows.append(count)
      artist_count+=1
  response={ "count": artist_count}

  record= []

  for artist, count_iter in zip(artists, count_shows):
      artist_dict = {
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": count_iter
        }
      record.append(artist_dict)
  response['data'] = record
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
    shows = db.session.query(Show.artist_id.label('artist_id'), (Venue.name).label('venue_name'), (Venue.image_link).label('venue_image_link'),Show.start_time).filter_by(artist_id=artist_id).join(Venue).all()
    past_shows = []
    upcoming_shows = []
    for show in shows:
      if show.start_time < datetime.now():
          past_shows.append(show)
      else:
          upcoming_shows.append(show)
    print(past_shows)
    artist = Artist.query.filter_by(id=artist_id).all()
    artist = artist[0]
    data = {
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "upcoming_shows_count": len(upcoming_shows),
      "past_shows_count": len(past_shows)
    }


    return render_template('pages/show_artist.html', artist=data)

@app.route('/artist/<artist_id>', methods=['POST'])
def delete_artist(artist_id):
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
 try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
 except:
     db.session.rollback()
     #flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
 finally:
      db.session.close()
 return redirect(url_for('artist'))
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.filter_by(id=artist_id).all()[0]
  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }
  form = ArtistForm()
  form.process(data=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.filter_by(id=artist_id).all()[0]
  try:
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.genres = request.form['genres']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.image_link = request.form['image_link']
      artist.facebook_link = request.form['facebook_link']
      artist.website = request.form['website']
      artist.seeking_venue = request.form['seeking_venue'] == 'True'
      artist.seeking_description = request.form['seeking_description']
    # on successful db insert, flash success
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully edited!')
  except:
     db.session.rollback()
     flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).all()[0]
  record={
    "id": venue.id,
    "name": venue.name,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  form.process(data=record)
  return render_template('forms/edit_venue.html', form=form, venue=record)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
   venue = Venue.query.filter_by(id=venue_id).all()[0]
   try:
       venue.name = request.form['name']
       venue.city = request.form['city']
       venue.state = request.form['state']
       venue.address = request.form['address']
       venue.phone = request.form['phone']
       venue.image_link = request.form['image_link']
       venue.facebook_link = request.form['facebook_link']
       venue.website = request.form['website']
       venue.seeking_talent = request.form['seeking_talent'] == 'True'
       venue.seeking_description = request.form['seeking_description']
     # on successful db insert, flash success
       db.session.commit()
       flash('Venue ' + request.form['name'] + ' was successfully edited!')
   except:
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
   finally:
       db.session.close()
   return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form

 try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      phone = request.form['phone']
      genres = request.form['genres']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website = request.form['website']
      seeking_venue = request.form['seeking_venue'] == 'True'
      seeking_description = request.form['seeking_description']

      artist = Artist(name = name, city = city, state=state,
                    phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link,
                    website = website, seeking_venue=seeking_venue, seeking_description=seeking_description)
    # on successful db insert, flash success
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
 except:
     db.session.rollback()
     flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
 finally:
      db.session.close()
 return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    show_list = db.session.query(Show, Artist, Venue).join(Artist).join(Venue).all()#(Venue,Show.venue_id==Venue.id).join(Artist, Show.artist_id==Artist.id).all()
    num_shows = db.session.query((Venue.id).label('id'),func.count(Show.id).label('count')).join(Venue).group_by(Venue.id).all()

    for show in show_list:
        for num_show in num_shows:
            if(num_show.id == show.Show.venue_id):
                record = {
                    "venue_id": show.Show.venue_id,
                    "venue_name": show.Venue.name,
                    "artist_id": show.Show.artist_id,
                    "artist_name": show.Artist.name,
                    "artist_image_link": show.Artist.image_link,
                    "start_time": show.Show.start_time,
                    "num_shows": num_show.count
                }
        print(record)
        data.append(record)

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
   try:
        venue_id = request.form['venue_id']
        artist_id = request.form['artist_id']
        start_time = request.form['start_time']

        show = Show(venue_id = venue_id, artist_id = artist_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
   except:
       db.session.rollback()
       flash('An error occurred. Show could not be listed.')
   finally:
        db.session.close()
  # on successful db insert, flash success
   return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

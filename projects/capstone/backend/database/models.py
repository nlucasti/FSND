from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.orm import backref
#UNCOMMENT IF NOT USING HEROKU
#database_path='postgresql://postgres:Shoobie1!@localhost:5432/fsnd-casting-app'
database_path = os.environ['DATABASE_URL']

#database_filename = "database.db"
#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movies
Have title and release year
'''
class Casts(db.Model):
    __tablename__ = 'Casts'

    id = Column(Integer, primary_key=True)
    movie_id = db.Column(Integer, db.ForeignKey('Movies.id',  ondelete="CASCADE"), nullable = False)
    actor_id = db.Column(Integer, db.ForeignKey('Actors.id',  ondelete="CASCADE"), nullable = False)

    actors = db.relationship("Actors", foreign_keys=[actor_id],  backref=backref("Casts", cascade="all,delete"))

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def format(self):
        return {
          'id': self.id,
          'movie_id': self.movie_id,
          'actor_id': self.actor_id}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Movies(db.Model):
  __tablename__ = 'Movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(DateTime)
  img_link = Column(String)
  # cast = db.relationship('Casts', backref='Movies', lazy=True, passive_deletes=True)

  #actors = db.relationship('Actors', backref='Movies', lazy=True, passive_deletes=True)

  def __init__(self, title, release_date, img_link):#, actors):
    self.title = title
    self.release_date = release_date
    self.img_link = img_link
    #self.actors = actors

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
      "img_link": self.img_link
      #"actors": self.actors
      }

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()

'''
Actors
Have name, age, and gender
'''

class Actors(db.Model):
  __tablename__ = 'Actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  # cast = db.relationship('Casts', backref='Movies', lazy=True, passive_deletes=True)
  casts = db.relationship('Casts', backref= 'Actors', passive_deletes=True)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

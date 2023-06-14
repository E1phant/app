from datetime import datetime as dt

from core import db
from models.base import Model
from models.relations import association

class Actor(Model, db.Model):
    __tablename__ = 'actors'

    # id -> integer, primary key
    id = db.Column(db.Integer, primary_key=True)
    # name -> string, size 50, unique, not nullable
    name = db.Column(db.String(50), unique=True, nullable=False)
    # gender -> string, size 11
    gender = db.Column(db.String(11))
    # date_of_birth -> date
    date_of_birth = db.Column(db.Date, default=dt(1900, 1, 1))

    # Use `db.relationship` method to define the Actor's relationship with Movie.
    # Set `backref` as 'cast', uselist=True
    # Set `secondary` as 'association'
    movies = db.relationship('Movie', backref='cast', uselist=True, secondary=association)

    def __repr__(self):
        return '<Actor {}>, <Gender {}>, <Date of birth {}>'.format(self.name, self.gender, self.date_of_birth)
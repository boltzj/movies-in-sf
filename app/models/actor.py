from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    # Many-to-Many relationship Actor / Movie
    movies = db.relationship("Movie",
                             secondary=lambda: actor_movie,
                             backref="actors")

    def __init__(self, name):
        self.name = name

    def get_information(self):
        return {
            'name': self.name
        }


# Association Table for Actor / Movie
actor_movie = Table('actor_movie', db.metadata,
                    Column('actor_id', Integer, ForeignKey('actor.id')),
                    Column('movie_id', Integer, ForeignKey('movie.id')))

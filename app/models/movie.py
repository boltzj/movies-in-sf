from app import db
from app.models.actor import Actor

from flask import jsonify


# Movie SQLAlchemy model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    release_year = db.Column(db.Integer)
    production = db.Column(db.String(255))
    distributor = db.Column(db.String(255))

    # Relationship
    locations = db.relationship('Location', backref='movie', lazy='dynamic')

    # Foreign Keys
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))

    def __init__(self, title, release_year, production, distributor):
        self.title = title
        self.release_year = release_year
        self.production = production
        self.distributor = distributor

    def add_director(self, director_id):
        self.director_id = director_id

    def add_writer(self, writer_id):
        self.writer_id = writer_id

    def add_actor(self, actor):
        # If actor is a string, try to find the actor in DB
        if actor.__class__ == str:
            actor = Actor.query.filter(Actor.name == actor).first()
        # Add actor to the movie
        if actor.__class__ == Actor:
            self.actors.append(actor)
        # Raise a Value error if not found or invalid
        else:
            raise ValueError

    def to_json(self):
        return jsonify({
            'id': self.id,
            'Title': self.title,
            'Release Year': self.release_year,
            'Production Company': self.production,
            'Distributor': self.distributor,
        })

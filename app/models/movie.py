from app import db

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
    actor1_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    actor2_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    actor3_id = db.Column(db.Integer, db.ForeignKey('actor.id'))

    def __init__(self, title, release_year, production, distributor):
        self.title = title
        self.release_year = release_year
        self.production = production
        self.distributor = distributor

    def add_director(self, director_id):
        self.director_id = director_id

    def add_writer(self, writer_id):
        self.writer_id = writer_id

    def add_actor1(self, actor1_id):
        self.actor1_id = actor1_id

    def add_actor2(self, actor2_id):
        self.actor2_id = actor2_id

    def add_actor3(self, actor3_id):
        self.actor3_id = actor3_id

    def to_json(self):
        return jsonify({
            'id': self.id,
            'Title': self.title,
            'Release Year': self.release_year,
            'Production Company': self.production,
            'Distributor': self.distributor,
        })

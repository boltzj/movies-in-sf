from app import db


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # Relationship
    movies = db.relationship('Movie', backref='writer', lazy='dynamic')

    def __init__(self, name):
        self.name = name

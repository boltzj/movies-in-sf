from app import db


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # Relationship
    movies = db.relationship('Movie', backref='director', lazy='dynamic')

    def __init__(self, name):
        self.name = name

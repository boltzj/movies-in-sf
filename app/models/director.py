from app import db


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)

    # Relationship
    movies = db.relationship('Movie', backref='director', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def get_information(self):
        return {
            'name': self.name
        }

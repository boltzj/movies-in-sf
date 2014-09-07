from app import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    fun_facts = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # Relations
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __init__(self, name, fun_facts, movie_id):
        self.name = name
        self.fun_facts = fun_facts
        self.movie_id = movie_id

    def get_information(self):
        return {
            'title': self.movie.title,
            'content': self.fun_facts,
            'location': self.name,
            'lat': self.latitude,
            'lng': self.longitude
        }

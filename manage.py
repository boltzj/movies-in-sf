#!/usr/bin/env python

import os

# Try to get the env var from .env file
if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from flask.ext.script import Manager, Shell

# Try to get the config name from the environment or use the default
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def test():
    """
    Run the unit tests.
    """
    import unittest

    # Look for existing tests in the 'tests' folder
    tests = unittest.TestLoader().discover('tests')

    # Run the tests
    unittest.TextTestRunner().run(tests)


# Import data from csv in the database
@manager.command
def import_db():
    """
    Import data from data.csv in the database
    :return:
    """
    import csv
    import os

    from app.models.movie import Movie
    from app.models.location import Location
    from app.models.director import Director
    from app.models.writer import Writer
    from app.models.actor import Actor

    db.drop_all()
    db.create_all()

    try:
        with open(os.path.dirname(__file__) + 'data/data.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            # Init dictionaries
            movies = dict()
            actors = dict()
            writers = dict()
            directors = dict()

            # FIXME : test header !
            header = reader.__next__()
            if header[0] != 'Title' or header[1] != 'Release Year':
                return "Bad File.."

            for row in reader:

                # Read CSV line
                title = row[0]
                release_year = row[1]
                location = row[2]
                fun_facts = row[3]
                production = row[4]
                distributor = row[5]
                director = row[6]
                writer = row[7]
                actor1 = row[8]
                actor2 = row[9]
                actor3 = row[10]

                if title not in movies:
                    # Create a new Movie
                    movie = Movie(title, release_year, production, distributor)

                    # Add director
                    if '' != director:
                        if director not in directors:
                            director = Director(director)
                            db.session.add(director)
                            db.session.flush()

                            # Save director information
                            directors[director.name] = {
                                'id': director.id,
                                'name': director.name,
                            }
                            # add director_id to movie
                            movie.add_director(director.id)
                        else:
                            movie.add_director(directors[director]['id'])

                    # Add writer
                    if '' != writer:
                        if writer not in writers:
                            writer = Writer(writer)
                            db.session.add(writer)
                            db.session.flush()

                            # Save director information
                            writers[writer.name] = {
                                'id': writer.id,
                                'name': writer.name,
                            }
                            # add director_id to movie
                            movie.add_writer(writer.id)
                        else:
                            movie.add_writer(writers[writer]['id'])

                    # Add actor 1
                    if '' != actor1:
                        if actor1 not in actors:
                            actor = Actor(actor1)
                            db.session.add(actor)
                            db.session.flush()

                            # Save director information
                            actors[actor1] = {
                                'id': actor.id,
                                'name': actor.name,
                            }

                            # add director_id to movie
                            movie.add_actor1(actor.id)
                        else:
                            movie.add_actor1(actors[actor1]['id'])

                    # Add actor 2
                    if '' != actor2:
                        if actor2 not in actors:
                            actor = Actor(actor2)
                            db.session.add(actor)
                            db.session.flush()

                            # Save director information
                            actors[actor2] = {
                                'id': actor.id,
                                'name': actor.name,
                            }

                            # add director_id to movie
                            movie.add_actor2(actor.id)
                        else:
                            movie.add_actor2(actors[actor2]['id'])

                    # Add actor 3
                    if '' != actor3:
                        if actor3 not in actors:
                            actor = Actor(actor3)
                            db.session.add(actor)
                            db.session.flush()

                            # Save director information
                            actors[actor3] = {
                                'id': actor.id,
                                'name': actor.name,
                            }

                            # add director_id to movie
                            movie.add_actor3(actor.id)
                        else:
                            movie.add_actor3(actors[actor3]['id'])


                    db.session.add(movie)
                    db.session.flush()

                    movies[title] = {
                        'Title': title,
                        'Release Year': release_year,
                        'Production Company': production,
                        'Distributor': distributor,
                        'id': movie.id
                    }

                    # Create new Location if not empty
                    if '' != location:
                        new_location = Location(location, fun_facts, movie.id)
                        new_location.geocode(0)
                        db.session.add(new_location)

                # Movie already exists, create new Location
                else:
                    if '' != location:
                        new_location = Location(location, fun_facts, movies[title]['id'])
                        new_location.geocode(0)
                        db.session.add(new_location)
    except FileNotFoundError:
        print("File : `" + os.path.dirname(__file__) + '/data/data.csv' + '` not found')

    db.session.commit()

# Run a Python shell with the App context
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

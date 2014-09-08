from app import db
import csv
from app.models.movie import Movie
from app.models.location import Location
from app.models.director import Director
from app.models.writer import Writer
from app.models.actor import Actor


def import_data_from_csv(file_path):
    """
    Import data from a csv file into database
    :return:
    """

    db.drop_all()
    db.create_all()

    try:
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

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
                title = row[0].strip()
                location = row[2]
                fun_facts = row[3]

                # Movie already exists create new location
                if title in movies:
                    if '' != location:
                        new_location = Location(location, fun_facts, movies[title]['id'])
                        db.session.add(new_location)
                    continue

                # Read more information from csv line about movie
                release_year = row[1]
                production = row[4]
                distributor = row[5]
                director = row[6]
                writer = row[7]
                movie_actors = [row[8], row[9], row[10]]

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

                # Add Actors
                for actor_name in movie_actors:
                    if actor_name != '':
                        if actor_name not in actors:
                            actor = Actor(actor_name)
                            db.session.add(actor)
                            db.session.flush()

                            # Save director information
                            actors[actor_name] = {
                                'id': actor.id,
                                'name': actor.name,
                            }

                            # add actor to movie
                            movie.add_actor(actor)
                        else:
                            movie.add_actor(actor_name)

                # Add Movie in DB
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
                    db.session.add(new_location)

            # Commit imported data
            db.session.commit()

    except FileNotFoundError:
        print("File : `" + file_path + '` not found')

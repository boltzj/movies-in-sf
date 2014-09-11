from app import db
import csv
from app.models.movie import Movie
from app.models.location import Location
from app.models.director import Director
from app.models.writer import Writer
from app.models.actor import Actor


def import_data_from_database():
    """
    Build dictionaries from database
    :return:
    """
    # Init dictionaries
    movies, actors, writers, directors, locations = {}, {}, {}, {}, {}

    for movie in Movie.query.all():
        # Save director information
        movies[movie.name] = movie.id

    for actor in Actor.query.all():
        # Save actor information
        actors[actor.name] = actor.id

    for writer in Writer.query.all():
        # Save writer information
        writers[writer.name] = writer.id

    for director in Director.query.all():
        # Save director information
        directors[director.name] = director.id

    for location in Location.query.all():
        locations[(location, location.movie_id)] = location.id

    return movies, actors, writers, directors, locations


def import_data_from_csv(file_path):
    """
    Import data from a csv file into database
    :return:
    """

    try:
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            # Init dictionaries
            movies, actors, writers, directors, locations = import_data_from_database()

            # FIXME : test header !
            header = next(reader)
            if header[0] != 'Title' or header[1] != 'Release Year':
                return "Bad File.."

            for row in reader:

                # Read CSV line
                name = row[0].strip()
                location = row[2]
                fun_facts = row[3]

                # Movie already exists create new location
                if name in movies:
                    if '' != location:
                        new_location = Location(location, fun_facts, movies[name])
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
                movie = Movie(name, release_year, production, distributor)

                # Add director
                if '' != director:
                    if director not in directors:
                        director = Director(director)
                        db.session.add(director)
                        db.session.flush()

                        # Save director id in local dictionary
                        directors[director.name] = director.id

                        # add director_id to movie
                        movie.add_director(director.id)
                    else:
                        movie.add_director(directors[director])

                # Add writer
                if '' != writer:
                    if writer not in writers:
                        writer = Writer(writer)
                        db.session.add(writer)
                        db.session.flush()

                        # Save director information
                        writers[writer.name] = writer.id

                        # add director_id to movie
                        movie.add_writer(writer.id)
                    else:
                        movie.add_writer(writers[writer])

                # Add Actors
                for actor_name in movie_actors:
                    if actor_name != '':
                        if actor_name not in actors:
                            actor = Actor(actor_name)
                            db.session.add(actor)
                            db.session.flush()

                            # Save director information
                            actors[actor_name] = actor.id

                            # add actor to movie
                            movie.add_actor(actor)
                        else:
                            movie.add_actor(actor_name)

                # Add Movie in DB
                db.session.add(movie)
                db.session.flush()

                # Store movie id in local dictionary
                movies[name] = movie.id

                # Create new Location, if not empty and does not exist
                if '' != location:
                    if (location, movie.id) not in locations:
                        new_location = Location(location, fun_facts, movie.id)
                        db.session.add(new_location)
                        db.session.flush()

                        locations[(location, movie.id)] = new_location.id

            # Commit imported data
            db.session.commit()

    except FileNotFoundError:
        print("File : `" + file_path + '` not found')

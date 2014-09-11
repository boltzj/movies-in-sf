#!/usr/bin/env python3
import os

# Try to get the env var from .env file
if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from flask.ext.script import Manager, Shell
from app.utils.import_data import import_data_from_csv
from app.utils.geocoder import geocode_database_locations

# Try to get the config name from the environment or use the default
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    # Add flask application (app) and Database (db) in the Python shell
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
def import_db(force=False):
    """
    Import database data from cvs file
    :return:
    """

    # FIXME: Init database from scratch (with '--force')
    # db.drop_all()
    # db.create_all()

    # Path of cvs file
    csv_path = (os.path.dirname(__file__) or '.') + '/data/data.csv'

    # Import locations from cvs file
    import_data_from_csv(csv_path)

    # Geocode locations in database
    geocode_database_locations(force)


# Run a Python shell with the App context
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

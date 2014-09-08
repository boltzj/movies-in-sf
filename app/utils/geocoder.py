from app.models.location import Location

from app import db
from googlegeocoder import GoogleGeocoder
import sys
import logging
import time

# Logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def location_geocode(location, attempt):
    """

    :param location:
    :param attempt:
    :return:
    """
    # initialize Google Geocoder
    geocoder = GoogleGeocoder()

    # location must be a class or subclass of Location
    if isinstance(location.__class__, Location):
        raise ValueError

    location_full_name = location.name + ', San Francisco, CA'

    try:
        logging.info('Geocoding: ' + location_full_name)

        # Get result from Google Maps API
        search = geocoder.get(location_full_name)

        if search.__len__() > 0:
            logging.info(search[0])
            location.latitude = search[0].geometry.location.lat
            location.longitude = search[0].geometry.location.lng
            db.session.commit()

    except ValueError as error:
        # Get message from error
        msg = str(error)

        if msg == 'OVER_QUERY_LIMIT':
            logging.info('OVER_QUERY_LIMIT, sleep for one second')
            time.sleep(1)
            if attempt < 5:
                location_geocode(location, attempt + 1)
            else:
                logging.error('Check your daily quota...')

        elif msg == 'ZERO_RESULTS':
            logging.warning('No result for: ' + location_full_name)

        else:
            logging.error('Google geocoder : ValueError: ', msg)

    # FIXME : geocoder.get() raise urllib.error.HTTPError: HTTP Error 500: Internal Server Error
    # except urllib.error.HTTPError as http_error:
    # urllib.error.URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known>


def geocode_database_locations():
    # Get locations from database
    locations = Location.query.all()

    for location in locations:
        # Get position from Google Maps API
        location_geocode(location, attempt=1)
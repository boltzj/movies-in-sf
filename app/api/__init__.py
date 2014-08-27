from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import errors
from app.api import movies
from app.api import locations
from app.api import directors
from app.api import writers
from app.api import actors


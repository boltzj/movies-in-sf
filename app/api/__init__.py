from flask import Blueprint

api = Blueprint('api', __name__)

from . import movies
from . import locations
from . import directors
from . import writers
from . import actors

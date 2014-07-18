sf-movie-api
============

Python / Flask / SQLAlchemy / API / SF_DATA

SF movies backend implementation

Build with Python and Flask

This my first project with Python + Flask, I've choose Python because most of Uber back-end uses it.
Flask is a quick and powerful framework to make an API

API Routes
============

/movies
/movie/<int:movie_id>
/movie/<int:movie_id>/locations
/movie/name

/directors
/director/<int:director_id>/locations
/director/name

/writers
/writer/<int:writer_id>/locations
/writer/name

/actors
/actor/<int:actor_id>/locations
/actor/name

/locations

# sf-movies
---

## Description
---

Python / Flask / SQLAlchemy / API / SF_DATA

**SF movies locations API implementation**

**Build with Python and Flask**


## Installation
---
To load data in the database:  
In a shell run :  
```
python manage.py import_db
```


## API Routes
---

### /movies
    List all movies names

### /movie/<int:movie_id>
    Get information for a movie
    
### /movie/<int:movie_id>/locations
    Get Locations for a movie
    
### /movie/name

### /directors
    List all directors names
    
### /director/<int:director_id>/locations

### /director/name

### /writers
    List all writers names
    
### /writer/<int:writer_id>/locations

### /writer/name

### /actors
    List all actors names
    
### /actor/<int:actor_id>/locations

### /actor/name

### /locations

# movies-in-sf

## Description

Python / Flask / SQLAlchemy

**SF movies locations API implementation**

**Build with _Python_ and _Flask_**


## Installation

### Local Installation

#### Requirements
 - python3.4.1  
 - virtualenv [install virtualenv](http://flask.pocoo.org/docs/0.10/installation/#virtualenv "Flask doc")  

#### Let's go
In your favorite terminal:  

Create a new virtual environment:  
```
$ virtualenv -p `which python3` venv
```

Activate it (You must source the virtualenv environment for each terminal session where you wish to run your app):  
```
. venv/bin/activate
```

Install the requirements:  
```
$ pip install -r requirements.txt
```

Import data from the cvs file in the database:      
```
$ python manage.py import_db
```

Run the tests (Optional):
```
$ python manage.py test
```

Run the dev server:
```
$ python manage.py runserver
```


### Production deploy
To run the application with gunicorn:  

Install production requirements:  
```
$ pip install -r requirements/prod.txt
```

set the environment variables or write it in an '.env' file in the top folder:  
```
FLASK_CONFIG=production
DATABASE_URL={protocol}[+{driver}]://{user}:{password}@{host}/{database}"
```

Run the gunicorn server:  
```
$ gunicorn manage:app
```

### Heroku deploy

#### Prerequisite

    Install Toolbelt
    
    Heroku Login
    
    Upload ssh public key

#### Let's go

Create app

Provisioning database

Promote database

add a Procfile

Push project on heroku
```
$ git push heroku master
```

Add a dyno

#### More info

[Deploying Python on Heroku](http://devcenter.heroku.com/articles/python "Getting Started with Python on Heroku")

## API Routes

#### /locations
	Get all locations

#### /movies
    Get all movie titles

#### /movies/\<name>
	Get information about a movie

#### /movies/\<name>/locations
	Get all locations for a movie

#### /directors
    Get all director names
    
#### /directors/\<name>
	Get information about a director

#### /directors/\<name>/movies
	Get all director movies

#### /directors/\<name>/locations
	Get all director's movie locations

#### /writers
    Get all writer names
    
#### /writers/\<name>
	Get information about a writer

#### /writers/\<name>/movies
	Get all writer's movies

#### /writers/\<name>/locations
	Get all writer's movie locations

#### /actors
    Get all actors names
    
#### /actors/\<name>
	Get information about an actor

#### /actors/\<name>/movies
	Get all actor's movies

#### /actors/\<name>/locations
	Get all actor's movie locations

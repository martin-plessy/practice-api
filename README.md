# A CRUD API to Practice Flask and Python

A CRUD API to practice Flask and Python, which I created before implementing [the Full Fibre's technical test](https://github.com/martin-plessy/technical-test), in order to learn the patterns of documenting, implementing and testing a green-field Flask API and forge my own opinion about Flask and its ecosystem.

## Project Requirements

The _Practice CRUD API_ uses __Python 3.8__.

## Project Setup

```ps1
# Virtual environment:
py -m venv .venv
./.venv/Scripts/Activate.ps1

# Installing project dependencies:
pip install -r requirements.txt

# You may also need:
pip install -e .
```

## Run the Tests

```ps1
# Tests:
pytest

# Tests with coverage:
coverage run -m pytest ; coverage report
```

## Run the App

```ps1
# Create the database schema:
flask create-db

# Start the development server:
$Env:FLASK_DEBUG = 1 ; flask run

# Fill the database with sample data:
flask fill-db
```

## Resources

- https://flask.palletsprojects.com/en/2.0.x/
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/
- https://marshmallow.readthedocs.io/en/stable/
- https://docs.sqlalchemy.org/en/14/orm/tutorial.html
- https://flask-restplus.readthedocs.io/en/stable/
- https://flask-restx.readthedocs.io/en/latest/
- https://flask-smorest.readthedocs.io/en/latest/
- https://github.com/tecladocode/rest-apis-flask-python
- https://www.mscharhag.com/api-design/rest-many-to-many-relations
- https://www.mscharhag.com/api-design/rest-one-to-many-relations
- https://github.com/lafrech/flask-smorest-sqlalchemy-example
- https://github.com/picsouds/flask-smorest-example-bookmanager
- And more...

## Notes

- I'm still much confused about the Flask-RestFull / Flask-RestPlus / Flask-RestX / Flask-SmoRest struggle...
- There seems to be a part of the Flask API that isn't documented (e.g. `flask.views.MethodView`).
- When adding new API resources, it's better to:
    1. Add it as an independent resource, i.e. without relations/FKs/links.
    2. Test the validation and other features for the _basic_ resource.
    3. Commit.
    4. And **only then** add the relations to other API resources.

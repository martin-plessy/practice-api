from flask_smorest import Blueprint
from webargs.flaskparser import FlaskParser

class CustomParser(FlaskParser):
    DEFAULT_VALIDATION_STATUS = 400

class ApiBlueprint(Blueprint):
    ARGUMENTS_PARSER = CustomParser()

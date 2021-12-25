from flask_smorest import Blueprint
from marshmallow import post_dump, Schema
from typing import Any, Mapping
from webargs.flaskparser import FlaskParser

class CustomParser(FlaskParser):
    DEFAULT_VALIDATION_STATUS = 400

class ApiBlueprint(Blueprint):
    ARGUMENTS_PARSER = CustomParser()

class ApiSchema(Schema):
    @post_dump
    def remove_none_values(self, data:  Mapping[str, Any], **kwargs):
        return {
            key: value
                for key, value in data.items()
                    if value is not None
        }

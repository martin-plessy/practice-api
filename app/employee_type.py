from app.db import db
from flask import Blueprint, jsonify, request
from marshmallow import fields, post_load, Schema, validate, ValidationError
from sqlalchemy.exc import IntegrityError
from typing import Any, List, Mapping

class EmployeeType(db.Model):
    uid = db.Column(db.Integer(), primary_key = True)
    type = db.Column(db.String(50), nullable = False, unique = True)

class EmployeeTypeSchema(Schema):
    uid = fields.Int(required = False, validate = [ validate.Range(min = 1) ])
    type = fields.Str(required = True, validate = [ validate.Length(min = 1, max = 50) ])

    @post_load
    def dict_to_object(self, data: Mapping[str, Any], **kwargs) -> EmployeeType:
        return EmployeeType(**data)

schema = EmployeeTypeSchema()
blueprint = Blueprint("employee_type", __name__)

@blueprint.route("/", methods = [ "GET" ])
def get_all():
    employee_types: List[EmployeeType] = EmployeeType.query.all()

    return schema.dumps(employee_types, many = True), 200, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/<int:id>", methods = [ "GET" ], )
def get_one(id: int):
    employee_type: EmployeeType = EmployeeType.query.get_or_404(id)

    return schema.dumps(employee_type, many = False), 200, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/", methods = [ "POST" ])
def post_one():
    try:
        employee_type: EmployeeType = schema.loads(request.data, many = False)
    except ValidationError as error:
        return error.messages, 400

    try:
        db.session.add(employee_type)
        db.session.commit()
    except IntegrityError:
        return { 'type': [ 'Value must be unique.' ] }, 409

    return schema.dumps(employee_type, many = False), 201, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/<int:id>", methods = [ "PUT" ])
def put_one(id: int):
    try:
        employee_type: EmployeeType = schema.loads(request.data, many = False)
        employee_type.uid = id
    except ValidationError as error:
        return error.messages, 400

    existing_employee_type: EmployeeType = EmployeeType.query.get_or_404(id)

    try:
        existing_employee_type.type = employee_type.type
        db.session.commit()
    except IntegrityError:
        return { 'type': [ 'Value must be unique.' ] }, 409

    return schema.dumps(existing_employee_type, many = False), 200, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/<int:id>", methods = [ "DELETE" ])
def delete_one(id: int):
    EmployeeType.query.filter(EmployeeType.uid == id).delete()
    db.session.commit()

    return jsonify(), 204

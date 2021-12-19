import marshmallow
from app.db import db
from flask import request
from flask_restx import Resource
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

class EmployeeTypeCollection(Resource):
    def get(self):
        employee_types: List[EmployeeType] = EmployeeType.query.all()

        return schema.dump(employee_types, many = True), 200

    def post(self):
        try:
            employee_type: EmployeeType = schema.loads(request.data, many = False)
        except ValidationError as error:
            return error.messages, 400

        try:
            db.session.add(employee_type)
            db.session.commit()
        except IntegrityError:
            return { 'type': [ 'Value must be unique.' ] }, 409

        return schema.dump(employee_type, many = False), 201

class EmployeeTypeItem(Resource):
    def get(self, id: int):
        employee_type: EmployeeType = EmployeeType.query.get_or_404(id)

        return schema.dump(employee_type, many = False), 200

    def put(self, id: int):
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

        return schema.dump(existing_employee_type, many = False), 200

    def delete(self, id: int):
        EmployeeType.query.filter(EmployeeType.uid == id).delete()
        db.session.commit()

        return '', 204

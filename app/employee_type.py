from app.db import db
from flask import request
from flask_restx import fields, Namespace, Resource
from marshmallow import post_load, Schema, validate, ValidationError
from marshmallow.fields import Int, Str
from sqlalchemy.exc import IntegrityError
from typing import Any, List, Mapping

class EmployeeType(db.Model):
    uid = db.Column(db.Integer(), primary_key = True)
    type = db.Column(db.String(50), nullable = False, unique = True)

class EmployeeTypeSchema(Schema):
    uid = Int(required = False, validate = [ validate.Range(min = 1) ])
    type = Str(required = True, validate = [ validate.Length(min = 1, max = 50) ])

    @post_load
    def dict_to_object(self, data: Mapping[str, Any], **kwargs) -> EmployeeType:
        return EmployeeType(**data)

schema = EmployeeTypeSchema()

employee_type_ns = Namespace("employee-type")

employee_type_input = employee_type_ns.model('EmployeeType_input', {
    'type': fields.String()
})

class EmployeeTypeCollection(Resource):
    def get(self):
        employee_types: List[EmployeeType] = EmployeeType.query.all()

        return schema.dump(employee_types, many = True), 200

    @employee_type_ns.expect(employee_type_input)
    def post(self):
        try:
            employee_type: EmployeeType = schema.loads(request.data, many = False)
            employee_type.uid = None
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

    @employee_type_ns.expect(employee_type_input)
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

employee_type_ns.add_resource(EmployeeTypeCollection, '/')
employee_type_ns.add_resource(EmployeeTypeItem, '/<int:id>')

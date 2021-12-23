from app.api import ApiBlueprint
from app.db import FkReference, db
from flask.views import MethodView
from flask_smorest import abort
from marshmallow import fields, post_load, Schema, validate
from sqlalchemy.exc import IntegrityError
from typing import Any, Mapping

class EmployeeType(db.Model):
    uid = db.Column(db.Integer(), primary_key = True)
    type = db.Column(db.String(50), nullable = False, unique = True)

class Employee(db.Model):
    uid = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(70), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    telephone = db.Column(db.String(32), nullable = False)

    employee_type_uid = db.Column(db.Integer(), db.ForeignKey('employee_type.uid'), nullable = False)
    employee_type = db.relationship('EmployeeType')

class EmployeeTypeSchema(Schema):
    uid = fields.Int(required = True, validate = [ validate.Range(min = 1) ], dump_only = True)
    type = fields.Str(required = True, validate = [ validate.Length(min = 1, max = 50) ])

    @post_load
    def dict_to_object(self, data: Mapping[str, Any], **kwargs):
        return EmployeeType(**data)

class EmployeeSchema(Schema):
    uid = fields.Int(required = True, validate = [ validate.Range(min = 1) ], dump_only = True)
    name = fields.Str(required = True, validate = [ validate.Length(min = 1, max = 70) ])
    email = fields.Str(required = True, validate = [ validate.Length(min = 1, max = 255) ]) # More validation should be put in place here,
    telephone = fields.Str(required = True, validate = [ validate.Length(min = 1, max = 32) ]) # but let's keep it out of scope to simplify.

    employee_type_uid = fields.Int(required = True, validate = [ FkReference(EmployeeType) ], load_only = True)
    employee_type = fields.Nested(EmployeeTypeSchema, required = True, dump_only = True)

    @post_load
    def dict_to_object(self, data: Mapping[str, Any], **kwargs):
        return Employee(**data)

bp = ApiBlueprint('Employees', __name__)

@bp.route('/employee-types/')
class EmployeeTypeCollection(MethodView):
    @bp.response(200, EmployeeTypeSchema(many = True))
    def get(self):
        return db.session.query(EmployeeType).all()

    @bp.arguments(EmployeeTypeSchema)
    @bp.response(201, EmployeeTypeSchema)
    def post(self, employee_type: EmployeeType):
        try:
            db.session.add(employee_type)
            db.session.commit()

        except IntegrityError:
            abort(409, errors = {
                'json': {
                    'type': [ 'Value must be unique.' ]
                }
            })

        return employee_type

@bp.route('/employee-types/<int:id>')
class EmployeeTypeItem(MethodView):
    @bp.response(200, EmployeeTypeSchema)
    def get(self, id: int):
        return db.session.query(EmployeeType).get_or_404(id)

    @bp.arguments(EmployeeTypeSchema)
    @bp.response(200, EmployeeTypeSchema)
    def put(self, employee_type: EmployeeType, id: int):
        existing_employee_type: EmployeeType = db.session.query(EmployeeType).get_or_404(id)

        try:
            existing_employee_type.type = employee_type.type
            db.session.commit()

        except IntegrityError:
            abort(409, errors = {
                'json': {
                    'type': [ 'Value must be unique.' ]
                }
            })

        return existing_employee_type

    @bp.response(204)
    def delete(self, id: int):
        if db.session.query(db.session.query(Employee).filter(Employee.employee_type_uid == id).exists()).scalar():
            abort(409, message = 'Employee type still has attached employees.')

        db.session.query(EmployeeType).filter(EmployeeType.uid == id).delete()
        db.session.commit()

@bp.route('/employees/')
class EmployeeCollection(MethodView):
    @bp.response(200, EmployeeSchema(many = True))
    def get(self):
        return db.session.query(Employee).all()

    @bp.arguments(EmployeeSchema)
    @bp.response(201, EmployeeSchema)
    def post(self, employee_type: Employee):
        db.session.add(employee_type)
        db.session.commit()

        return employee_type

@bp.route('/employees/<int:id>')
class EmployeeItem(MethodView):
    @bp.response(200, EmployeeSchema)
    def get(self, id: int):
        return db.session.query(Employee).get_or_404(id)

    @bp.arguments(EmployeeSchema)
    @bp.response(200, EmployeeSchema)
    def put(self, employee_type: Employee, id: int):
        existing_employee_type: Employee = db.session.query(Employee).get_or_404(id)

        existing_employee_type.name = employee_type.name
        existing_employee_type.email = employee_type.email
        existing_employee_type.telephone = employee_type.telephone
        existing_employee_type.employee_type_uid = employee_type.employee_type_uid
        db.session.commit()

        return existing_employee_type

    @bp.response(204)
    def delete(self, id: int):
        db.session.query(Employee).filter(Employee.uid == id).delete()
        db.session.commit()

from app.db import open_db
from flask import Blueprint, jsonify, request
from marshmallow import fields, post_load, Schema, validate, ValidationError
from sqlite3 import IntegrityError, Row
from typing import Any, Dict, List, Mapping, Tuple, Union

class EmployeeType:
    def __init__(self, uid: int = -1, type: str = 0):
        self.uid = uid
        self.type = type

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
    employee_types = open_db().execute("""
        SELECT employee_type.uid, employee_type.type
        FROM employee_type
    """).fetchall()

    return schema.dumps(employee_types, many = True), 200, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/<int:id>", methods = [ "GET" ], )
def get_one(id: int):
    employee_type = open_db().execute("""
        SELECT employee_type.uid, employee_type.type
        FROM employee_type
        WHERE uid = ?
    """, (id, )).fetchone()

    if employee_type is None:
        return { 'title': 'not found' }, 404
    else:
        return schema.dumps(employee_type, many = False), 200, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/", methods = [ "POST" ])
def post_one():
    try:
        employee_type: EmployeeType = schema.loads(request.data, many = False)
    except ValidationError as error:
        return error.messages, 400

    try:
        db = open_db()

        employee_type.uid = db.execute("""
            INSERT INTO employee_type (type)
            VALUES (?)
        """, (employee_type.type, )).lastrowid

        db.commit()

    except IntegrityError:
        return { 'type': [ 'Value must be unique.' ] }, 409

    else:
        return schema.dumps(employee_type, many = False), 201, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/<int:id>", methods = [ "PUT" ])
def put_one(id: int):
    try:
        employee_type: EmployeeType = schema.loads(request.data, many = False)
        employee_type.uid = id
    except ValidationError as error:
        return error.messages, 400

    try:
        db = open_db()

        updates = db.execute("""
            UPDATE employee_type
            SET type = ?
            WHERE uid = ?
        """, (employee_type.type, employee_type.uid, )).rowcount

        db.commit()

    except IntegrityError:
        return { 'type': [ 'Value must be unique.' ] }, 409

    else:
        if updates == 0:
            return { 'title': 'not found' }, 404
        else:
            return schema.dumps(employee_type, many = False), 200, { 'Content-Type': 'application/json; charset=utf-8' }

@blueprint.route("/<int:id>", methods = [ "DELETE" ])
def delete_one(id: int):
    db = open_db()

    db.execute("""
        DELETE FROM employee_type
        WHERE uid = ?
    """, (id, ))

    db.commit()

    return jsonify(), 204

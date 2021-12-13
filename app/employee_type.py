from app.db import open_db
from flask import Blueprint, jsonify, request
from sqlite3 import IntegrityError, Row
from typing import Any, Dict, List, Tuple, Union

blueprint = Blueprint("employee_type", __name__)

def _row_to_dict(row: Row) -> Dict[str, Any]:
    return {
        'uid': row['uid'],
        'type': row['type']
    }

def _rows_to_list(rows: List[Row]) -> List[Dict[str, Any]]:
    return [ _row_to_dict(row) for row in rows ]

@blueprint.route("/", methods = [ "GET" ])
def get_all():
    data = open_db().execute("""
        SELECT employee_type.uid, employee_type.type
        FROM employee_type
    """).fetchall()

    return jsonify(_rows_to_list(data))

@blueprint.route("/<int:id>", methods = [ "GET" ])
def get_one(id: int):
    data = open_db().execute("""
        SELECT employee_type.uid, employee_type.type
        FROM employee_type
        WHERE uid = ?
    """, (id, )).fetchone()

    if data is None:
        return {
            'title': 'not found'
        }, 404

    return _row_to_dict(data), 200

@blueprint.route("/", methods = [ "POST" ])
def post_one():
    type = request.json.get('type', None)

    is_valid, error_code, error_response = _validate(type)

    if not is_valid:
        return error_response, error_code

    try:
        db = open_db()

        uid = db.execute("""
            INSERT INTO employee_type (type)
            VALUES (?)
        """, (type, )).lastrowid

        db.commit()

    except IntegrityError as e:
        return {
            'title': 'conflict',
            'invalid-params': [
                { 'name': 'type', 'reason': 'duplicated' }
            ]
        }, 409

    else:
        return {
            'uid': uid,
            'type': type
        }, 201

@blueprint.route("/<int:id>", methods = [ "PUT" ])
def put_one(id: int):
    type = request.json.get('type', None)

    is_valid, error_code, error_response = _validate(type)

    if not is_valid:
        return error_response, error_code

    try:
        db = open_db()

        updates = db.execute("""
            UPDATE employee_type
            SET type = ?
            WHERE uid = ?
        """, (type, id, )).rowcount

        db.commit()

    except IntegrityError as e:
        return {
            'title': 'conflict',
            'invalid-params': [
                { 'name': 'type', 'reason': 'duplicated' }
            ]
        }, 409

    else:
        if updates == 0:
            return {
                'title': 'not found'
            }, 404

        return {
            'uid': id,
            'type': type
        }, 200

@blueprint.route("/<int:id>", methods = [ "DELETE" ])
def delete_one(id: int):
    db = open_db()

    db.execute("""
        DELETE FROM employee_type
        WHERE uid = ?
    """, (id, ))

    db.commit()

    return jsonify(), 204

def _validate(type: Union[str, None]) -> Tuple[bool, Union[int, None], Union[Dict[str, Any], None]]:
    if type is None:
        return False, 400, {
            'title': 'bad request',
            'invalid-params': [
                { 'name': 'type', 'reason': 'required' }
            ]
        }

    if not isinstance(type, str):
        return False, 400, {
            'title': 'bad request',
            'invalid-params': [
                { 'name': 'type', 'reason': 'must be string' }
            ]
        }

    if len(type) == 0:
        return False, 400, {
            'title': 'bad request',
            'invalid-params': [
                { 'name': 'type', 'reason': 'required' }
            ]
        }

    if 50 < len(type):
        return False, 400, {
            'title': 'bad request',
            'invalid-params': [
                { 'name': 'type', 'reason': 'max length exceeded' }
            ]
        }

    return True, None, None

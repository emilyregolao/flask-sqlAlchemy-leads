from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy import exc
from app.controllers.json_controller import validate_keys, is_valid_phone
from app.models.leads_model import Lead
from app.configs.database import db

def create_lead():
    data = request.get_json()
    
    valid_keys, invalid_keys = validate_keys(data)
    received_keys = [key for key in data.keys()]

    if invalid_keys:
        return jsonify({"error": "invalid keys", "expected": valid_keys, "received": received_keys}), HTTPStatus.BAD_REQUEST

    try:
        
        if not is_valid_phone(data['phone']):
            return jsonify({"error": "phone data in wrong format", "expected format": ["(xx)xxxxx-xxxx"], "received": [data['phone']]}), HTTPStatus.BAD_REQUEST
        
        lead = Lead(
            name = data['name'],
            email = data['email'],
            phone = data['phone']
        )
        db.session.add(lead)
        db.session.commit()
        return jsonify(lead), HTTPStatus.CREATED

    except exc.IntegrityError as _:
        return jsonify({"error": "phone or email already exists in database"}), HTTPStatus.BAD_REQUEST

    except TypeError as _: 
        return jsonify({"error": "all values must be of type string"}), HTTPStatus.BAD_REQUEST


def get_leads():
    ...

def update_lead():
    ...

def delete_lead():
    ...
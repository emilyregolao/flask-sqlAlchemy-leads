from sqlalchemy.orm.session import Session
from flask import request, jsonify
from datetime import datetime
from http import HTTPStatus
from sqlalchemy import exc, desc
from app.controllers.json_controller import validate_keys, is_valid_phone, is_valid_data_type, is_valid_email_key
from app.models.leads_model import Lead
from app.configs.database import db

def create_lead():
    data = request.get_json()

    valid_keys, invalid_keys = validate_keys(data)
    if invalid_keys:
        return jsonify({"error": "invalid keys", "expected": valid_keys, "received": list(data.keys())}), HTTPStatus.BAD_REQUEST

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
    try:
        session: Session = db.session
        base_query = session.query(Lead)
        leads = base_query.order_by(desc(Lead.visits)).all()
    except:
        return jsonify({"error": "no data found"}), HTTPStatus.NOT_FOUND
    return jsonify(leads), HTTPStatus.OK


def update_lead():
    data = request.get_json()
   
    if not is_valid_data_type(data):    
        return jsonify({"data": "the value must be of type string"}), HTTPStatus.BAD_REQUEST
    if not is_valid_email_key(data):
        return jsonify({"error": "wrong key(s)", "expected": ["email"], "received": list(data.keys())}), HTTPStatus.BAD_REQUEST

    try:        
        email = list(data.values())[0]
        
        session: Session = db.session
        lead = session.query(Lead).filter(Lead.email == email).first()
        lead.visits = lead.visits + 1
        lead.last_visit = datetime.now()
        
        db.session.commit()
        return "", HTTPStatus.OK

    except:
        return jsonify({"error": "email not found in database"}), HTTPStatus.NOT_FOUND

def delete_lead():
    ...
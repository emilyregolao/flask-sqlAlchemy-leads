from sqlalchemy.orm.session import Session
from flask import request, jsonify
from datetime import datetime
from http import HTTPStatus
from sqlalchemy import exc, desc
from app.controllers.json_controller import validate_keys, is_valid_phone, is_valid_data_type, is_valid_email_key
from app.models.leads_model import Lead
from app.configs.database import db


# POST ROUTE CONTROLLER 
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


# GET ROUTE CONTROLLER 
def get_leads():
    try:
        session: Session = db.session
        base_query = session.query(Lead)
        leads = base_query.order_by(desc(Lead.visits)).all()
    except:
        return jsonify({"error": "no data found"}), HTTPStatus.NOT_FOUND
    return jsonify(leads), HTTPStatus.OK


# UPDATE ROUTE CONTROLLER 
def update_lead():
    data = request.get_json()
    session: Session = db.session
    base_query = session.query(Lead)
   
    if not is_valid_data_type(data):    
        return jsonify({"data": "the value must be of type string"}), HTTPStatus.BAD_REQUEST
    if not is_valid_email_key(data):
        return jsonify({"error": "wrong key(s)", "expected": ["email"], "received": list(data.keys())}), HTTPStatus.BAD_REQUEST

    email = list(data.values())[0]
    updated_lead = base_query.filter(Lead.email == email).first()

    if not updated_lead:
        return jsonify({"error": "email not found in database"}), HTTPStatus.NOT_FOUND

    updated_lead.visits = updated_lead.visits + 1
    updated_lead.last_visit = datetime.now()
    session.commit()

    return "", HTTPStatus.OK


# DELETE ROUTE CONTROLLER 
def delete_lead():
    data = request.get_json()
    session: Session = db.session
    base_query = session.query(Lead)
   
    if not is_valid_data_type(data):    
        return jsonify({"data": "the value must be of type string"}), HTTPStatus.BAD_REQUEST
    if not is_valid_email_key(data):
        return jsonify({"error": "wrong key(s)", "expected": ["email"], "received": list(data.keys())}), HTTPStatus.BAD_REQUEST

    email = list(data.values())[0]
    deleted_lead = base_query.filter(Lead.email == email).first()

    if not deleted_lead:
        return jsonify({"error": "email not found in database"}), HTTPStatus.NOT_FOUND

    session.delete(deleted_lead)
    session.commit()

    return "", HTTPStatus.OK
    

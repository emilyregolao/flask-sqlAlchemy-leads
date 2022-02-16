from flask import Blueprint
from app.controllers.leads_controller import create_lead, get_leads, update_lead, delete_lead

leads_bp = Blueprint("leads", __name__, url_prefix="/leads")

leads_bp.post("")(create_lead)

leads_bp.get("")(get_leads)

leads_bp.patch("")(update_lead)

leads_bp.delete("")(delete_lead)
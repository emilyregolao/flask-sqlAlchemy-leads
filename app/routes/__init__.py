from flask import Blueprint, Flask
from app.routes.leads_routes import leads_bp

api_bp = Blueprint("api", __name__)

def init_app(app: Flask):
    api_bp.register_blueprint(leads_bp)
    app.register_blueprint(api_bp)
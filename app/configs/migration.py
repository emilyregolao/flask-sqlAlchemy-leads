from flask import Flask
from app.configs.database import db
from flask_migrate import Migrate

def init_app(app: Flask):
    Migrate(app, db, compare_type=True)
#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal
from ..models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from werkzeug.security import check_password_hash

#Blueprint for settings
settings_bp = Blueprint('settings_bp', __name__)
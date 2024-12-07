from flask import Blueprint, request, jsonify
from ..models import User
from datetime import datetime
from app import db
from werkzeug.security import check_password_hash

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            join_date=datetime.now(),
            points=0,
            level=1
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            raise ValueError()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise ValueError()

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return jsonify({"success": True, "message": "Login successful"})
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    
    
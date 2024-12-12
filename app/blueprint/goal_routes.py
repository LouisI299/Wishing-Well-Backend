#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

#Make a Blueprint for goals
goal_bp = Blueprint('goal_bp', __name__)

#Routes

#Route for getting all goals
# @goal_bp.route('/all', methods=['GET'])
# def get_goals():
#     goals = SavingsGoal.query.all()
#     return jsonify([goal.serialize() for goal in goals])

#Route for getting a goal by ID
@goal_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_goal(id):
    try:
        goal = SavingsGoal.query.get(id)
        if goal:
            return jsonify(goal.serialize())
        else:
            return jsonify({"error": "Goal not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


#Route for getting current user goals
@goal_bp.route('/user', methods=['GET'])
@jwt_required()
def getCurrentUser_goals():
    try : 
        user_id = get_jwt_identity()
        
        savingsGoals = SavingsGoal.query.filter_by(user_id=user_id).all()
        
        return jsonify([goal.serialize() for goal in savingsGoals]), 200
       
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    

#route for creating a goal 
@goal_bp.route('/', methods=['POST'])
@jwt_required()
def create_goal():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No data provided")
        
        goal_data = SavingsGoal(**data)
    
        user_id = get_jwt_identity()
        start_date = datetime.now()
        end_date = datetime.strptime(goal_data.end_date, '%Y-%m-%d')  # Convert end_date string to datetime object

        new_goal = SavingsGoal(
            name=goal_data.name,
            target_amount=goal_data.target_amount,
            current_amount=goal_data.current_amount,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            category=goal_data.category,
            period_amount=goal_data.period_amount,
            status=goal_data.status,
            saving_method=goal_data.saving_method
        )

        db.session.add(new_goal)
        db.session.commit()

        return jsonify(new_goal.serialize()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Route for updating a goal by ID
@goal_bp.route('/<int:id>', methods=['PUT']) 
@jwt_required()
def update_goal(id):
    try:
        data = request.get_json()
        goal = SavingsGoal.query.get(id)
        if not goal:
            return jsonify({"error": "Goal not found"}), 404

        goal.name = data.get('name', goal.name)
        goal.target_amount = data.get('target_amount', goal.target_amount)
        goal.current_amount = data.get('current_amount', goal.current_amount)
        goal.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        goal.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')

        db.session.commit()
        return jsonify(goal.serialize()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Route for deleting a goal by ID
@goal_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_goal(id):
    try:
        goal = SavingsGoal.query.get(id)
        if not goal:
            return jsonify({"error": "Goal not found"}), 404

        db.session.delete(goal)
        db.session.commit()
        return jsonify({"message": "Goal deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

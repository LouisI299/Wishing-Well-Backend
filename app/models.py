#Imports
from app import db
from werkzeug.security import generate_password_hash
from pydantic import BaseModel, EmailStr, StringConstraints, constr
from typing_extensions import Optional, Annotated

#User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)
    
    #Constructor for making a new user
    def __init__(self, first_name, last_name, email, password, join_date, points, level):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password) #Hash the password
        self.join_date = join_date
        self.points = points
        self.level = level
    
    #Function to serialize the user object
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'join_date': self.join_date,
            'points': self.points,
            'level': self.level
        }
    
#Savings goal model
class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    target_amount = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, nullable=False)
    period_amount = db.Column(db.Integer, nullable=False) #Monthly or weekly amount
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    saving_method = db.Column(db.Boolean, nullable=False, default=True) #Monthly = 1, Weekly = 0
    status = db.Column(db.Boolean , nullable=False, default=True) #In Progress = 1, Completed = 0
    
    #Function to serialize the goal object
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'period_amount': self.period_amount,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'saving_method': self.saving_method,
            
            'status': self.status
        }
    
#Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('savings_goal.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'goal_id': self.goal_id,
            'amount': self.amount,
            'transaction_date': self.transaction_date,
            'type': self.type
        }
        
#Pydantic model for validating login data
class UserLoginModel(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    
    
#Pydantic model for creating a new user
class UserCreateModel(BaseModel):
    first_name: constr(min_length=2, max_length=50)
    last_name: constr(min_length=2, max_length=50)
    email: EmailStr
    password: constr(min_length=6)
    
#Pydantic model for creating a new goal
class GoalCreateModel(BaseModel):
    name: constr(min_length=2, max_length=50)
    target_amount: int
    current_amount: Optional[float] = 0
    end_date: str
    category: constr(min_length=2, max_length=50)
    period_amount: Optional[float] = 0
    saving_method: bool
    

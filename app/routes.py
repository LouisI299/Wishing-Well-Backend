from flask import Flask
from app.blueprint.user_routes import user_bp
from app.blueprint.goal_routes import goal_bp

def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(goal_bp, url_prefix='/api/goals')
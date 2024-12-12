#Imports
from flask import Flask, send_from_directory
from app.blueprint.user_routes import user_bp
from app.blueprint.goal_routes import goal_bp
from app.blueprint.transaction_routes import transaction_bp
from app.blueprint.settings_routes import settings_bp
from werkzeug.exceptions import NotFound

#Register blueprints
def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(goal_bp, url_prefix='/api/goals')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react_app(path):
        if path.startswith("api"):
            raise NotFound()  
        try:
            return send_from_directory(app.static_folder, "index.html")
        except FileNotFoundError:
            return {"error": "React app not found. Build the frontend!"}, 404
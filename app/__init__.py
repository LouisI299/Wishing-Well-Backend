from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('instance.config.Config')
    
    
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    # Extensions
    db.init_app(app)
    
    with app.app_context():
        from app import models
        db.create_all()
        db.session.commit()

    # Blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
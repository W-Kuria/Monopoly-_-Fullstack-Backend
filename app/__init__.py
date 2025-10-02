from flask import Flask
from .config import Config
from .db import db,migrate
from app.routes import auth_bp
from flask_cors import CORS  


def create_app():

        app= Flask(__name__)
        app.config.from_object(config.Config)

        db.init_app(app)
       
        migrate.init_app(app,db)
        CORS(app)  
        
        # Register blueprints
        from app.routes.auth import auth_bp
        from app.routes.game import game_bp  # Add this line
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(game_bp)  # Add this line
        
        return app
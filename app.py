from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from Models import db
import os

# Load env
load_dotenv()

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Enable CORS (for all routes and origins by default)
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)



    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from Routes.auth import auth_bp
    from Routes.game import game_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)

    return app

# Import models so Flask-Migrate can detect them
from Models import *


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # create tables if not exist
    app.run(debug=True,port=5500)

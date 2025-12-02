from flask import Flask
from config import Config
from app.extensions import db, jwt
from flask_migrate import Migrate
from flask_cors import CORS  # ADD THIS

from app.routes.auth import auth_bp
from app.routes.user import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------------------------------------------------
    # ENABLE CORS FOR ANGULAR (FIX FOR YOUR ISSUE)
    # ---------------------------------------------------
    CORS(app,
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")

    return app

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from app.extensions import db, jwt

from app.routes.auth import auth_bp

migrate = Migrate()   # <- MUST BE GLOBAL for migrations

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for Angular
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)   # <- FIXED!

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")

    return app

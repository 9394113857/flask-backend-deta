from flask import Flask
from config import Config
from app.extensions import init_extensions
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize DB, JWT, Migrate
    init_extensions(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")

    return app

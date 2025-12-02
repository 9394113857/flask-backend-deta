import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import pytz   # timezone support

# ----------------------------------------------------
# APP INITIALIZATION
# ----------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)


# ----------------------------------------------------
# HOME ROUTE — SHOW IST & UTC WITH FLAGS IN TABLE FORMAT
# ----------------------------------------------------
@app.route("/")
def home():
    # Get UTC time (Railway server time)
    utc_now = datetime.now(pytz.utc)

    # Convert to India IST
    india_tz = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.astimezone(india_tz)

    # Table output
    time_table = [
        {
            "sno": 1,
            "country": "United Kingdom / UTC",
            "flag": "🇬🇧",
            "time": utc_now.strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "sno": 2,
            "country": "India (IST)",
            "flag": "🇮🇳",
            "time": ist_now.strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

    return {
        "message": "Flask API is live with CI/CD Auto Deploy",
        "deployment_table": time_table,
        "environment": os.environ.get("RAILWAY_ENVIRONMENT", "Local Machine")
    }


# ----------------------------------------------------
# DATABASE MODEL
# ----------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(255))


# ----------------------------------------------------
# ERROR HANDLER
# ----------------------------------------------------
def handle_error(e):
    if isinstance(e, IntegrityError):
        message = str(e.orig)

        if "UNIQUE constraint failed" in message:
            if "user.username" in message:
                return {"error": "Username already exists"}, 400
            if "user.email" in message:
                return {"error": "Email already exists"}, 400
            if "user.phone" in message:
                return {"error": "Phone already exists"}, 400

        return {"error": "Database integrity error", "details": message}, 400

    if isinstance(e, SQLAlchemyError):
        return {"error": "Database error", "details": str(e)}, 500

    return {"error": "Unexpected server error", "details": str(e)}, 500


# ----------------------------------------------------
# REGISTER ROUTE
# ----------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data.get("username"):
            return {"error": "username is required"}, 400
        if not data.get("password"):
            return {"error": "password is required"}, 400

        hashed = generate_password_hash(data["password"])

        user = User(
            username=data["username"],
            password=hashed,
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address")
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "Registered successfully"}, 201

    except Exception as e:
        db.session.rollback()
        return handle_error(e)


# ----------------------------------------------------
# LOGIN ROUTE
# ----------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data.get("username") or not data.get("password"):
            return {"error": "username and password required"}, 400

        user = User.query.filter_by(username=data["username"]).first()

        if not user:
            return {"error": "Username not found"}, 404

        if not check_password_hash(user.password, data["password"]):
            return {"error": "Incorrect password"}, 401

        token = create_access_token(identity=user.id)

        return {"access_token": token}

    except Exception as e:
        return handle_error(e)


# ----------------------------------------------------
# PROFILE ROUTE (Protected)
# ----------------------------------------------------
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        }

    except Exception as e:
        return handle_error(e)


# ----------------------------------------------------
# START SERVER
# ----------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

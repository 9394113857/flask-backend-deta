import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(255))

# ROUTES
@app.route("/")
def home():
    return {"message": "Flask API on Railway is running — small update deployed via CI/CD."}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return {"message": "Username already exists"}, 400

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

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return {"message": "Invalid credentials"}, 401

    token = create_access_token(identity=user.id)
    return {"access_token": token}

@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user = User.query.get(get_jwt_identity())
    if not user:
        return {"message": "Not found"}, 404

    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address
    }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

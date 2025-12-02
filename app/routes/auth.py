from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/")
def home():
    return {"message": "Flask API running with migrations"}

@auth_bp.post("/register")
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return {"message": "Username exists"}, 400

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
    return {"message": "Registered"}, 201

@auth_bp.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    
    if not user or not check_password_hash(user.password, data["password"]):
        return {"message": "Invalid credentials"}, 401

    token = create_access_token(identity=user.id)
    return {"token": token}

@auth_bp.get("/profile")
@jwt_required()
def profile():
    user = User.query.get(get_jwt_identity())
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address
    }

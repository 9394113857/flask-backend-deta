from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import User
from app.extensions import db

user_bp = Blueprint("user", __name__)

# GET ALL USERS
@user_bp.get("/users")
def get_all_users():
    users = User.query.all()
    response = []
    for u in users:
        response.append({
            "id": u.id,
            "username": u.username,
            "name": u.name,
            "email": u.email,
            "phone": u.phone,
            "address": u.address
        })
    return jsonify(response), 200


# GET USER BY ID
@user_bp.get("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404

    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address
    }


# UPDATE USER
@user_bp.put("/users/<int:user_id>")
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404

    data = request.json
    user.name = data.get("name", user.name)
    user.address = data.get("address", user.address)

    db.session.commit()
    return {"message": "User updated successfully"}, 200


# DELETE USER
@user_bp.delete("/users/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}, 200

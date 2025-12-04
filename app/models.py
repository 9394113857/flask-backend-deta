from app.extensions import db

class User(db.Model):
    __tablename__ = "users"  # 🔥 VERY IMPORTANT

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(255))

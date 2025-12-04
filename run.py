from app import create_app
from app.extensions import db
import os

# Create the Flask application
app = create_app()

<<<<<<< HEAD
# Railway/Gunicorn will use the 'app' variable automatically.
# No need for debug=True or host/port here.
=======
# ---------------------------------------------
# LOCAL DEVELOPMENT ONLY: Auto-create tables
# ---------------------------------------------
# Detect SQLite local environment
IS_LOCAL = "DATABASE_URL" not in os.environ

if IS_LOCAL:
    with app.app_context():
        db.create_all()
        print("✔ Local SQLite tables created.")

# ---------------------------------------------
# NORMAL FLASK RUN
# ---------------------------------------------
>>>>>>> feature/sqlalchemy-migrations
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

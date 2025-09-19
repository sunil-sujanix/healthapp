import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db,User,Document,Dependent,Record
from blueprints import routes

def create_app():
    app = Flask(__name__)

    # Database connection (from Render env)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT secret
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")

    # Allow CORS (React frontend URL will be set in env)
    CORS(app, resources={r"/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})

    # Init extensions
    db.init_app(app)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(routes)

    # Healthcheck route
    @app.get("/health")
    def health():
        return {"ok": True}

    # Create tables if not already present
    with app.app_context():
        from models import User, Dependent, Record, Document  # make sure all models are imported
        db.create_all()

    return app

# 👇 this is what Gunicorn will look for
app = create_app()

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated
    
    # 👇 Important: Import User after db is initialized
    from app.models import User

    # 🔑 This is REQUIRED — Flask-Login uses this to reload the user from the session
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Returns User object or None

    # Register blueprints
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app
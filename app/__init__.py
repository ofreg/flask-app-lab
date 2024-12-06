from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)    
migrate= Migrate()
bcrypt = Bcrypt() 
login_manager = LoginManager()
def create_app(config_name="config"):
    app=Flask(__name__)
    app.config.from_object(config_name)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    
    with app.app_context():
        login_manager.login_view = "users.login"  # Де маршрут для входу
        login_manager.login_message = "Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки."
        login_manager.login_message_category = "info"
        from . import views
        from .users.models import User
        from .posts import post_bp
        from .users import users_bp
        app.register_blueprint(post_bp)
        app.register_blueprint(users_bp, url_prefix="/users")
        #from app.posts.models import
    return app
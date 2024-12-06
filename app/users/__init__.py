from flask import Blueprint, current_app

users_bp = Blueprint("users",__name__,url_prefix="/users",template_folder="templates/users")

from . import views

from app import login_manager
from app.users.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


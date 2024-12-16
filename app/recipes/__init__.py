from flask import Blueprint

recipes_bp = Blueprint('recipes', __name__,template_folder='templates/recipes',static_folder="static",static_url_path='/recipes/static')   

from . import views
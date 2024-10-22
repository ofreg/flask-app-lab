from flask import Blueprint

post_bp = Blueprint("posts", __name__, url_prefix="/post",template_folder="templates/posts")

from . import views
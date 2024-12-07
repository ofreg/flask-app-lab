from app import db
from flask_login import UserMixin
import os
import secrets
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import datetime
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')  # Розширення шляху до зображення
    about_me = db.Column(db.String(500))  
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    # Функція для збереження зображення профілю
    def save_picture(self, form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

        form_picture.save(picture_path)

        return picture_fn

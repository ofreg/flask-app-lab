from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_login import UserMixin


bcrypt = Bcrypt()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

   
    recipes = db.relationship('Recipe', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.category_name}>"


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)  
    ingredients = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('recipe_users.id'), nullable=False)
    def __repr__(self):
        return f"<Recipe {self.name}>"





class RecipeUser(db.Model, UserMixin):
    __tablename__ = 'recipe_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)

    # Між таблицями RecipeUser і Recipe має бути зв'язок
    recipes = db.relationship('Recipe', backref='author', lazy=True)

    def __repr__(self):
        return f"<RecipeUser {self.name}>"

    # Хешування пароля
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Перевірка пароля
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import PasswordField, BooleanField
class RecipeForm(FlaskForm):
    name = StringField('Назва рецепту', validators=[DataRequired()])
    description = TextAreaField('Опис', validators=[DataRequired()])
    cooking_time = IntegerField('Час приготування', validators=[DataRequired()])
    ingredients = TextAreaField('Інгредієнти', validators=[DataRequired()])
    category_id = IntegerField('Категорія', validators=[DataRequired()])
    image = FileField('Фото рецепту')  # Поле для зображення
    submit = SubmitField('Додати рецепт')  


class RegistrationForm(FlaskForm):
    name = StringField('Ім’я', validators=[DataRequired()])
    email = StringField('Емейл', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердження пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватись')



class LoginForm(FlaskForm):
    email = StringField('Електронна пошта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')

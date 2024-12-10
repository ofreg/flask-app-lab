from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from app.users.models import User 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=14),Regexp(r'^[a-zA-Z0-9_.-]+$', message="Недопустимі символи в username.")])
    email = StringField ('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=6, message="Пароль має бути щонайменше 6 символів.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password', message="Паролі мають співпадати.")])
    profile_picture = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    

    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Цей email вже зареєстрований.")

    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Цей username вже зайнятий.")
class LoginForm(FlaskForm):
    email= StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Оновити фото профілю', validators=[FileAllowed(['jpg', 'png'])])
    about_me = StringField('About Me', validators=[Length(max=500)])
    submit = SubmitField('Оновити')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Цей username вже зайнятий.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Цей email вже зайнятий.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новий пароль', validators=[
        DataRequired(), Length(min=4)
    ])
    confirm_password = PasswordField('Підтвердження нового пароля', validators=[
        DataRequired(), EqualTo('new_password', message='Паролі повинні співпадати')
    ])
    submit = SubmitField('Змінити пароль')  # Додано поле submit

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from app.users.models import User 

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=14),Regexp(r'^[a-zA-Z0-9_.-]+$', message="Недопустимі символи в username.")])
    email = StringField ('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=6, message="Пароль має бути щонайменше 6 символів.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password', message="Паролі мають співпадати.")]
    )

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
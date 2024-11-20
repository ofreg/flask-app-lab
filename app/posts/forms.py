from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField,  DateField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime
CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = TextAreaField('Content', render_kw={"rows": 5,"cols":40},validators=[DataRequired()])
    is_active= BooleanField('Active Post')
    publish_date= DateTimeLocalField('Publish Date',format='%Y-%m-%dT%H:%M',default=datetime.now())
    category = SelectField('Category', choices=CATEGORIES,validators=[DataRequired()])
    author = StringField('author')
    submit = SubmitField('Add Post')

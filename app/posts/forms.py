from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField,  DateField, SelectField, DateTimeLocalField,SelectMultipleField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from .models import Tag
CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = TextAreaField('Content', render_kw={"rows": 5,"cols":40},validators=[DataRequired()])
    tags = SelectMultipleField(
        "Tags",
        coerce=int,
        choices=[(tag.id, tag.name) for tag in Tag.query.all()]  
    )
    is_active= BooleanField('Active Post')
    publish_date= DateTimeLocalField('Publish Date',format='%Y-%m-%dT%H:%M',default=datetime.now())
    category = SelectField('Category', choices=CATEGORIES,validators=[DataRequired()])
    author_id = SelectField("Author", coerce=int)

    submit = SubmitField('Add Post')

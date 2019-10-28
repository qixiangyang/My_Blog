"""
Description:
Author:qxy
Date: 2019/10/27 3:07 下午
File: forms 
"""


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Content', [DataRequired()])
    categories = SelectMultipleField('Categories', coerce=int)


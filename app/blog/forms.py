"""
Description:
Author:qxy
Date: 2019/10/27 3:07 下午
File: forms 
"""


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Content', [DataRequired()])
    category = StringField('Category', [DataRequired(), Length(max=255)])
    tags = StringField('Tags', [DataRequired(), Length(max=255)])


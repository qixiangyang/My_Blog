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
    title = StringField('标题', [DataRequired(), Length(max=255)])
    text = TextAreaField('内容', [DataRequired()])
    text_pre = TextAreaField('预览', [DataRequired()])
    category = StringField('分类', [DataRequired(), Length(max=255)])
    tags = StringField('标签', [DataRequired(), Length(max=255)])


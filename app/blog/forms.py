"""
Description:
Author:qxy
Date: 2019/10/27 3:07 下午
File: forms 
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):

    title = StringField('标题', [DataRequired(), Length(max=255)])
    create_time = DateTimeField('发表时间', [DataRequired()], format='%Y-%m-%d')
    text = TextAreaField('内容', [DataRequired()])
    text_pre = TextAreaField('内容概要', [DataRequired()])
    tags = StringField('标签', [DataRequired(), Length(max=255)], default="")
    category = SelectField('分类', [DataRequired()])
    save_script = SubmitField('存草稿')


class SourceForm(FlaskForm):
    blog_source = StringField('博客推荐', [DataRequired(), Length(max=255)])


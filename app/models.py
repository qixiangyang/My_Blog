"""
Description:
Author:qxy
Date: 2019/10/9 5:33 下午
File: models 
"""

from . import db


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), unique=True)
    text = db.Column(db.String(10000))
    author = db.Column(db.String(20))
    category = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    upload_time = db.Column(db.DateTime)
    other_info = db.Column(db.String(100))

    def __repr__(self):
        return '<title %r author %r>' % (self.title, self.author)
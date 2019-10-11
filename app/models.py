"""
Description:
Author:qxy
Date: 2019/10/9 5:33 下午
File: models 
"""

from . import db
import datetime


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), unique=True)
    text = db.Column(db.String(10000))
    author = db.Column(db.String(20))
    category = db.Column(db.String(20))
    tags = db.Column(db.String(50))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    upload_time = db.Column(db.DateTime)
    other_info = db.Column(db.String(100))

    def __repr__(self):
        return '<title %r author %r>' % (self.title, self.author)
    
    def to_json(self):
        json_data = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'author': self.author,
            'category': self.category,
            'tags': self.tags,
            'create_time': self.create_time.strftime('%Y-%m-%d'),
            'update_time': self.update_time.strftime('%Y-%m-%d'),
            'upload_time': self.upload_time.strftime('%Y-%m-%d'),
            'other_info': self.other_info
        }
        return json_data
    
    
class PyNews(db.Model):
    __tablename__ = 'pynews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), unique=True)
    text = db.Column(db.String())
    author = db.Column(db.String(20))
    category = db.Column(db.String(20))
    tags = db.Column(db.String(20))
    read_count = db.Column(db.Integer)
    pub_time = db.Column(db.DateTime)
    url = db.Column(db.String(100))
    other_info = db.Column(db.String(100))
    
    def __repr__(self):
        return '<title %r author %r>' % (self.title, self.author)

    def to_json(self):
        json_data = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'author': self.author,
            'category': self.category,
            'tags': self.tags,
            'read_count': self.read_count,
            'pub_time': self.pub_time.strftime('%Y-%m-%d'),
            'url': self.url,
            'other_info': self.other_info
        }
        return json_data

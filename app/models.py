"""
Description:
Author:qxy
Date: 2019/10/9 5:33 下午
File: models
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


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
            'create_time': str(self.create_time),
            'update_time': str(self.update_time),
            'upload_time': str(self.upload_time),
            'other_info': self.other_info,
        }
        return json_data


class PyNews(db.Model):
    __tablename__ = 'pynews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True)
    text = db.Column(db.String())
    preview = db.Column(db.String())
    author = db.Column(db.String(50))
    category = db.Column(db.String(100))
    tags = db.Column(db.String(200))
    read_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    pub_time = db.Column(db.DateTime)
    url = db.Column(db.String(100))
    other_info = db.Column(db.String(100))
    blog_name = db.Column(db.String(100))
    line = db.Column(db.String(100))

    def __repr__(self):
        return '<title %r author %r>' % (self.title, self.author)

    def to_json(self):
        json_data = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'preview': self.preview,
            'author': self.author,
            'category': self.category,
            'tags': self.tags,
            'read_count': self.read_count,
            'comment_count': self.comment_count,
            'pub_time': str(self.pub_time),
            'url': self.url,
            'other_info': self.other_info,
            'blog_name': self.blog_name,
            'line': self.line
        }
        return json_data


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

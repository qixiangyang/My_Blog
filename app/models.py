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
    text = db.Column(db.Text())
    text_pre = db.Column(db.String(500))
    author = db.Column(db.String(20))
    category = db.relationship('ArticleCategory')
    tags_record = db.relationship('ArticleTagsRecord')
    create_time = db.Column(db.TIMESTAMP)
    update_time = db.Column(db.TIMESTAMP)
    other_info = db.Column(db.String(100))
    status = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<title %r author %r>' % (self.title, self.author)

    def to_json(self):
        json_data = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'text_pre': self.text_pre,
            'author': self.author,
            'category': self.category.category_name,
            'tags': ' '.join(self.tags_record.tags_name),
            'create_time': self.create_time,
            'update_time': self.update_time,
            'other_info': self.other_info,
        }
        return json_data


class ArticleCategory(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(30))
    parent = db.relationship("Article", back_populates="child")


class ArticleTagsRecord(db.Model):
    __tablename__ = 'tags_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    tags_name = db.relationship('ArticleTags', backref=db.backref('tags'))
    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'))


class ArticleTags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tags_name = db.Column(db.String(30), nullable=False)


class PyNews(db.Model):
    __tablename__ = 'pynews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True)
    text = db.Column(db.Text())
    preview = db.Column(db.Text())
    author = db.Column(db.String(50))
    category = db.Column(db.String(100))
    tags = db.Column(db.String(200))
    read_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    pub_time = db.Column(db.TIMESTAMP)
    url = db.Column(db.String(280))
    other_info = db.Column(db.String(170))
    blog_name = db.Column(db.String(160))
    line = db.Column(db.String(150))
    status = db.Column(db.Integer, default=1)

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
            'pub_time': self.pub_time,
            'url': self.url,
            'other_info': self.other_info,
            'blog_name': self.blog_name,
            'line': self.line
        }
        return json_data


class Click(db.Model):
    __tablename__ = 'access_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route = db.Column(db.String(20))
    time = db.Column(db.TIMESTAMP)
    ip_address = db.Column(db.String(20))
    cookie = db.Column(db.String(200))
    user_agent = db.Column(db.String(200))


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

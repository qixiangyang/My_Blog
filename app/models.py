"""
Description:
Author:qxy
Date: 2019/10/9 5:33 下午
File: models
"""

import datetime

from sqlalchemy import and_
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class ArticleStatus:
    publish = 1
    script = 2
    delete = 3


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), unique=True)
    text = db.Column(db.Text())
    text_pre = db.Column(db.String(500))
    author = db.Column(db.String(20))
    other_info = db.Column(db.String(100))
    status = db.Column(db.Integer, default=ArticleStatus.publish)  # 1 正常 2. 草稿 3. 删除

    create_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # ont to many relation
    category_m = db.relationship(
        "ArticleCategory", uselist=True,
        primaryjoin="foreign(Article.id) == remote(ArticleCategory.article_id)"
    )

    tags = db.relationship(
        "ArticleTags", uselist=True,
        primaryjoin="foreign(Article.id) == remote(ArticleTags.article_id)"
    )

    def __repr__(self):
        return 'f<title {self.title} author {self.author}>'

    @property
    def category(self):
        return ";".join([x.json.get("category_name") for x in self.category_m])

    @property
    def tag(self):
        return ";".join([x.json.get("tag_name") for x in self.tags])

    def to_json(self):
        json_data = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'text_pre': self.text_pre,
            'author': self.author,
            'category': self.category,
            'tags': self.tag,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'other_info': self.other_info,
        }
        return json_data

    def creat_article_category(self, category_id_list: list):
        now_category_id_set = {x.category_id for x in self.category_m}
        new_category_id_set = set(category_id_list)
        if now_category_id_set == new_category_id_set:
            return
        for id_info in new_category_id_set - now_category_id_set:
            article_category_obj = ArticleCategory(article_id=self.id, category_id=id_info)
            db.session.add(article_category_obj)

        for id_info in now_category_id_set - new_category_id_set:

            ArticleCategory.query.filter(and_(
                ArticleCategory.article_id == self.id,
                ArticleCategory.category_id == id_info
            )).delete()

        db.session.commit()

    def creat_article_tag(self, tag_name_list: list):

        now_tag_name_set = {x.name for x in self.tags}
        new_tag_name_set = set(tag_name_list)
        if now_tag_name_set == new_tag_name_set:
            return
        for tag_name in new_tag_name_set - now_tag_name_set:
            article_tag_obj = ArticleTags(article_id=self.id, name=tag_name)
            db.session.add(article_tag_obj)

        for tag_name in now_tag_name_set - new_tag_name_set:

            ArticleTags.query.filter(and_(
                ArticleCategory.article_id == self.id,
                ArticleCategory.name == tag_name
            )).delete()

        db.session.commit()


class ArticleCategory(db.Model):
    __tablename__ = 'article_category_m'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    create_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # one to many
    category = db.relationship(
        "Category", uselist=False,
        primaryjoin="foreign(ArticleCategory.category_id) == remote(Category.id)"
    )

    @property
    def json(self):
        return {
            "category_id": self.category.id,
            "category_name": self.category.name,
        }


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500))
    extra = db.Column(db.String(500))
    create_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # one to many
    category_m = db.relationship(
        "ArticleCategory", uselist=True,
        primaryjoin="foreign(Category.id) == remote(ArticleCategory.category_id)"
    )

    @property
    def json(self):
        return {
            "category_id": self.id,
            "category_name": self.name,
            "extra": self.extra
        }

    @classmethod
    def get_all_category(cls):
        return [x.json for x in cls.query.all()]


class ArticleTags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    name = db.Column(db.String(500))
    create_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    @property
    def json(self):
        return {
            "tag_id": self.id,
            "tag_name": self.name,
        }


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


class AccessLog(db.Model):
    __tablename__ = 'access_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route = db.Column(db.String(200))
    request_method = db.Column(db.String(20))
    ip_address = db.Column(db.String(20))
    cookie = db.Column(db.Text)
    user_agent = db.Column(db.String(200))
    create_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    create_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_time = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)

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

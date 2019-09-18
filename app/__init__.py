"""
Description:
Author:qxy
Date: 2019/9/18 3:00 下午
File: __init__ 
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
 
bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)
    return app

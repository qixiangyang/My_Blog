"""
Description:
Author:qxy
Date: 2019/9/18 3:00 下午
File: __init__ 
"""
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from .filters import handle_time
from logging.handlers import TimedRotatingFileHandler
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'auth.login'


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "log/flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    app.jinja_env.filters['handle_time'] = handle_time

    return app


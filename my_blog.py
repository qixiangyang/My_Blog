import os
import logging
from flask_migrate import Migrate
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)
print(os.getenv('FLASK_ENV'))


if __name__ != '__main__':
    # 如果不是直接运行，则将日志输出到 gunicorn 中
    if app.config.get("PRODUCT"):
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        app.logger.setLevel('INFO')  # <<-特别注意，否则info级别不能打印

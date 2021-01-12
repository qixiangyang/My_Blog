import os
from flask_migrate import Migrate
from app import create_app, db


# print(os.getenv('FLASK_ENVIRONMENT'))
app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)


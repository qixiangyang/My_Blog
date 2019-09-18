import os
import click
from flask_migrate import Migrate
from app import create_app, db

app = create_app('default')
migrate = Migrate(app, db)




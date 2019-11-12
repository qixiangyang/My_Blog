import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import Article, PyNews, User, Role, Click

# print(os.getenv('FLASK_ENVIRONMENT'))
app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Article=Article, PyNews=PyNews, User=User,
                Role=Role, Click=Click)

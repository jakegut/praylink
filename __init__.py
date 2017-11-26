from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.scss import Scss

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

Scss(app, static_dir='static', asset_dir='assets')

#migrations
migrate = Migrate(app, db)

#import models
from prayer.models import Prayer
from member.models import Member

from prayer import views

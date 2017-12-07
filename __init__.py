from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.scss import Scss
from twilio.rest import Client

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

Scss(app, static_dir='static', asset_dir='assets')

#migrations
migrate = Migrate(app, db)

# Create Twilio client instance
account_sid = app.config["TWILIO_ACCOUNT_SID"]
auth_token = app.config["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

#import models
from prayer.models import Prayer, prayed_for
from member.models import Member

#Register Views
from prayer import views
from member import views

#Register Blueprints
from admin.views import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

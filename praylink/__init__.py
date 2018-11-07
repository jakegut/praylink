from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_scss import Scss
from twilio.rest import Client

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

Scss(app, static_dir='praylink/static', asset_dir='praylink/assets')

#migrations
migrate = Migrate(app, db)

# Create Twilio client instance
account_sid = app.config["TWILIO_ACCOUNT_SID"]
auth_token = app.config["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

#import models
from praylink.prayer.models import Prayer, prayed_for
from praylink.member.models import Member
from praylink.group.models import Group

#Register Views
from praylink.prayer import views
from praylink.member import views
from praylink.group import views

#Register Blueprints
from praylink.admin.views import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

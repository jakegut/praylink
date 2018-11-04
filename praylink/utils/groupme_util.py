import os
from praylink import app
from groupy.client import Client
client = Client.from_token(app.config["GROUPME_TOKEN"])

def add_to_groupme(prayer_content):
    return client.bots.list()[0].post(prayer_content)
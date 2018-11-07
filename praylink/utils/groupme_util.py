import os
from praylink import app, db
from praylink.group.models import Group
from groupy.client import Client
client = Client.from_token(app.config["GROUPME_TOKEN"])

def add_to_groupme(prayer_content, group):
    client = Client.from_token(group.groupme_token)
    for bot in client.bots.list():
        if bot.id == group.groupme_bid:
            return bot.post(prayer_content)
    return False

def create_group_bot(group_id, new_token=True):
    group = Group.query.filter_by(id=group_id).first()
    client = Client.from_token(group.groupme_token)
    
    if group.id is None:
        print("Couldn't find group to send GroupMe")
        return

    if new_token or group.groupme_bid is None:
        new_group = client.groups.create(name=("%s Prayer Group" % group.title))
        group.groupme_gid = new_group.id
        new_bot = client.bots.create("Prayer Bot", new_group.id)
        group.groupme_bid = new_bot.bot_id
        db.session.commit()
        new_bot.post("Hello from Praylink! This is a test of your GroupMe credentials. This is the group that urgent prayers will be sent to")
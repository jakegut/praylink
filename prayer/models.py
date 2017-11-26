from prayer_bot_flask import db
from datetime import datetime

class Prayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    prayer_count = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)
    update = db.Column(db.Text)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __init__(self, content, member, publish_date, update=None, prayer_count=0):
        self.content = content
        self.member_id = member.id
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.update = update
        self.prayer_count = prayer_count

    def __repr__():
        return '<Prayer %r>' % self.content

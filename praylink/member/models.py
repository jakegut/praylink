from prayer_bot_flask import db
from prayer.models import prayed_for

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean)
    token = db.Column(db.Integer)
    prayers = db.relationship('Prayer', backref="member", lazy="dynamic")
    prayed_for = db.relationship('Prayer', secondary=prayed_for, backref=db.backref('prayed_for', lazy='dynamic'))
    subscribe_digest = db.Column(db.Boolean)
    subscribe_prayed = db.Column(db.Boolean)

    def __init__(self, phone_number, password=None, is_admin=False, subscribe_digest=True, subscribe_prayed=True):
        self.phone_number = phone_number
        self.password = password
        self.is_admin = is_admin
        self.subscribe_digest = subscribe_digest
        self.subscribe_prayed = subscribe_prayed
    
    def __repr__(self):
        return "<Member %r>" % self.phone_number
from praylink import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    twilio_sid = db.Column(db.Text)
    twilio_token = db.Column(db.Text)
    twilio_number = db.Column(db.Text)
    groupme_token = db.Column(db.Text)
    groupme_gid = db.Column(db.Text)
    groupme_bid = db.Column(db.Text)

    def __init__(self, title, twilio_sid=None, twilio_token=None, twilio_number=None, groupme_token=None):
        self.title = title
        self.twilio_sid = twilio_sid
        self.twilio_token = twilio_token
        self.twilio_number = twilio_number
        self.groupme_token = groupme_token
        self.groupme_gid = None
        self.groupme_bid = None

    def __repr__(self):
        print("<Group %s>" % self.name)
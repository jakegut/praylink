from praylink import db
from datetime import datetime

class Prayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    prayer_count = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)
    update = db.Column(db.Text)
    report_count = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, content, member, group, publish_date, update=None, prayer_count=0, report_count=0):
        self.content = content
        self.member_id = member.id
        self.group_id = group.id
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.update = update
        self.prayer_count = prayer_count
        self.report_count = report_count

    def __repr__(self):
        return '<Prayer %r>' % self.content

prayed_for = db.Table('prayed_for',
    db.Column("member_id", db.Integer, db.ForeignKey('member.id')),
    db.Column("prayer_id", db.Integer, db.ForeignKey('prayer.id')),
    db.UniqueConstraint('member_id', 'prayer_id', name='unique')
)

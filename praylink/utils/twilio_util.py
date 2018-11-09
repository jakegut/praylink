from twilio.rest import Client
from praylink.member.models import Member

def send_twilio_test(group):
    client = Client(group.twilio_sid, group.twilio_token)
    member = Member.query.filter_by(is_admin=True).first()
    client.messages.create(
        to=member.phone_number,
        from_=group.twilio_number,
        body="This is a test to see if your Twilio Credentials are correct, so now you're good to go!"
    )

def send_twilio(group, member, message):
    client = Client(group.twilio_sid, group.twilio_token)
    client.messages.create(
        to = member.phone_number,
        from_=group.twilio_number,
        body=message
    )
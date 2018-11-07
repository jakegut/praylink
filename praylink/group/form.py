from flask_wtf import Form
from wtforms import validators, StringField, BooleanField
from wtforms.fields.html5 import TelField

class NewGroupForm(Form):
    group_name = StringField('Group Name', [
        validators.Required(),
        validators.Regexp('^[a-zA-Z0-9_ ]*$', message="Title must be alphnumeric (a-Z, 0-9)")
    ])

    twilio_sid = StringField('Twilio SID',[
        validators.Required()
    ])

    twilio_token = StringField('Twilio Token', [
        validators.Required()
    ])

    phone_number = TelField('Twilio Phone Number', [
        validators.Required()
    ])

    groupme_token = StringField('GroupMe Token', [
        validators.Required()
    ])


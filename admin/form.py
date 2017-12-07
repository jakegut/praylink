from flask_wtf import Form
from wtforms import validators, StringField

class EditPrayer(Form):
    content = StringField('Prayer Content', [
        validators.Required()
    ])
    update = StringField('Update')
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, IntegerField, BooleanField
from wtforms.fields.html5 import TelField

class PhoneField(Form):
    phone_number = TelField('Phone Number', [
        validators.Required(),
        validators.Regexp('^\d{3}-\d{3}-\d{4}$', message="Phone number must be in the format: xxx-xxx-xxxx")
        ])

class ValidateNumberForm(Form):
    code = IntegerField('Code', [
        validators.Required()
    ])

class PasswordForm(Form):
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message="Passwords must match"),
        validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')
    
class LoginForm(Form):
    phone_number = StringField('Phone Number', [
        validators.Required(),
        validators.Regexp('^\d{3}-\d{3}-\d{4}$', message="Phone number must be in the format: xxx-xxx-xxxx")
        ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=4, max=80)
        ])

class SettingsForm(Form):
    sub_digest = BooleanField('Subscribe to Digest',[
        validators.Required()
    ])
    sub_update = BooleanField('Subscribe to Updates on Prayer Requests',[
        validators.Required()
    ])

class EditPrayer(Form):
    content = StringField('Prayer Content', [
        validators.Required()
    ])
    update = StringField('Update')

class AddPrayer(Form):
    content = StringField('Prayer Content', [
        validators.Required()
    ])
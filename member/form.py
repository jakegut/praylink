from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, IntegerField
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
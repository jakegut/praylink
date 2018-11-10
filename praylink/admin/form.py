from flask_wtf import Form
from wtforms import validators, StringField, SelectField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class EditPrayer(Form):
    content = StringField('Prayer Content', [
        validators.Required()
    ])
    update = StringField('Update')

class GenerateForm(Form):
    type = SelectField('Type', 
        choices=[
            ('pdf', 'PDF'),
            ('html', 'HTML')
        ]
    )
    time_range = SelectField('Range',
        choices=[
            ('1', "Past Day"),
            ('7', "Past Week"),
            ('30', "Past Month"),
            ('365', "Past Year"),
            ('9999', "Beginning of Time")
        ]
    )
    columns = MultiCheckboxField('Columns', 
        choices=[
            ('phone_number', 'Phone Number'),
            ('content', 'Prayer'),
            ('update', "Update"),
            ('publish_date', 'Date Submitted'),
        ]
    )
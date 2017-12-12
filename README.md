# Praylink
A service that allows people to text in a prayer request.

## About
Came about as a way to gather prayer requests for a youth ministry.

## Features
Prayer requests are added to Google Spreadsheet, and if it's an "urgent" prayer it will also be sent to a GroupMe group. There is also a website where people can pray for prayer requests and create an account to get updates on the prayers they have prayed for. Admin functionality is available to edit and delete prayers.

## Installation
Praylink uses the Flask web framework, meaning that Python(3.6+) needs to be installed. It also uses celery for regular and periodic tasks, but it is not necessary for development unless certain features need to be tested.

1. It is prefered to use a vitrualenv for development, so follow steps to do that first
1. Activate virtualenv
1. Run `pip install -r requirements.txt`
1. Edit `settings.py` to make sure settings are right for Twilio and Google Sheets
1. A `.groupy.key` file in your home directory is needed for GroupMe to work, the only contents of the file are the GroupMe API key
1. A `client_secret.json` (or whatever) is required for Google Sheets to work, you get this from the Google API Developer console.
1. Run `python manage.py db init`
1. Run `python manage.py db migrate`
1. Run `python manage.py db upgrade`
1. Finally, run `python manage.py runserver`
1. If you're using celery, use the executable in your virtualenv, adapt as needed: `venv\Scripts\celery.exe -A tasks.celery_app worker -l info -P eventlet`
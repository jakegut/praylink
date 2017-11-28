import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from celery import Celery
from prayer_bot_flask import app, client
from prayer.models import Prayer
from member.models import Member


# COMMAND TO RUN (windows): venv\Scripts\celery.exe -A tasks.celery_app worker

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery_app = make_celery(app)

@celery_app.task
def send_update(prayer_id):
    prayer = Prayer.query.filter_by(id=prayer_id).first()
    members = prayer.prayed_for
    for member in members:
        client.messages.create(
                to=member.phone_number,
                from_=app.config['TWILIO_NUMBER'],
                body="A prayer you have prayed for ({}) has been updated: {}".format(prayer.content, prayer.update)
            )
    return True


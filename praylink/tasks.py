import datetime

from celery import Celery
from celery.schedules import crontab
from praylink import app, client
from praylink.prayer.models import Prayer
from praylink.member.models import Member

# COMMAND TO RUN CELERY BEAT (periodic tasks): venv\Scripts\celery.exe -A tasks:celery_app beat --loglevel=INFO
# COMMAND TO RUN CELERY (windows): venv\Scripts\celery.exe -A tasks.celery_app worker -P eventlet

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

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=00, hour=7, day_of_week=0),
        # 30.0,
        weekley_digest.s(),
        name='Weekly Digest'
    )

    sender.add_periodic_task(
        crontab(minute=00, hour=7, day_of_week=3),
        # 30.0,
        update_reminder.s(),
        name='Update Reminder'
    )
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

@celery_app.task
def weekley_digest():
    seven_days_ago = datetime.datetime.today() - datetime.timedelta(7)
    members = Member.query.filter_by(subscribe_digest=True).all()
    prayers = Prayer.query.filter(Prayer.publish_date >= seven_days_ago).order_by(Prayer.prayer_count.desc()).limit(5).all()

    resp = "Prayer Request digest for last week.\n\n"

    if prayers:
        for prayer in prayers:
            resp += ("\"" + prayer.content + "\", prayed for: " + str(prayer.prayer_count) + (" times", " time")[bool(prayer.prayer_count == 1)] + "\n")
    else:
        print("No prayers found!")

    resp += "\nVisit http://pray-link.com for more prayers. To unsubscribe, reply 'unsubscribe digest'"

    for member in members:
        client.messages.create(
            to=member.phone_number,
            from_=app.config['TWILIO_NUMBER'],
            body=resp
        )

@celery_app.task
def update_reminder():
    seven_days_ago = datetime.datetime.today() - datetime.timedelta(7)
    members = Member.query.all()

    for member in members:
        prayer = member.prayers.filter_by(update=None).filter(Prayer.publish_date >= seven_days_ago).first()
        if prayer:
            resp = "Your prayer: \'{}\' needs an update. Reply \'update {} [update here]\' to give everyone an update on your prayer!".format(prayer.content, prayer.id)
            client.messages.create(
                to=member.phone_number,
                from_=app.config['TWILIO_NUMBER'],
                body=resp
            )

@celery_app.task
def send_update(prayer_id):
    prayer = Prayer.query.filter_by(id=prayer_id).first()
    members = prayer.prayed_for.filter_by(subscribe_prayed=True).all()
    for member in members:
        client.messages.create(
                to=member.phone_number,
                from_=app.config['TWILIO_NUMBER'],
                body="A prayer you have prayed for ({}) has been updated: {}".format(prayer.content, prayer.update)
            )
    return True


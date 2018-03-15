from flask import request, render_template, jsonify, session
from prayer_bot_flask import app
from twilio.twiml.messaging_response import MessagingResponse
from prayer_bot_flask import db
from prayer_bot_flask.tasks import send_update
from sqlalchemy import exc
from profanity import profanity 
from prayer.models import Prayer
from member.models import Member
from utils.spreadsheet_util import add_to_spreadsheet
from utils.groupme_util import add_to_groupme

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    per_page = app.config['PER_PAGE']
    prayers = Prayer.query.order_by(Prayer.publish_date.desc()).paginate(page, per_page, False).items
    tmpl_name = 'prayer/index.html' if page == 1 else 'prayer/items.html'
    return render_template(tmpl_name, prayers=prayers, page=page)

@app.route('/prayed_for/<int:prayer_id>', methods=['POST'])
def prayed_for(prayer_id):
    prayer = Prayer.query.filter_by(id=prayer_id).first()
    if prayer.id:
        prayer.prayer_count += 1
        db.session.commit()
        if 'member_id' in session:
            member = Member.query.filter_by(id=session['member_id']).first()
            if member:
                prayer.prayed_for.append(member)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            return jsonify({'success': 'success', 'prayer_count': prayer.prayer_count})

        return jsonify({'success': 'success', 'prayer_count': prayer.prayer_count})
    else:
        return jsonify({'error': 'error'})

@app.route('/message', methods=['POST'])
def message():
    body = request.values.get('Body')
    phone_number = request.values.get('From')

    resp = MessagingResponse()

    member = Member.query.filter_by(phone_number=phone_number).first()

    if not member:
        new_member = Member(phone_number)
        db.session.add(new_member)
        db.session.flush()

        if new_member.id:
            db.session.commit()
            resp.message("Welcome to Central Baptist Youth Ministry's prayer request program. Text 'pray [prayer here]' to submit a prayer or 'commands' to learn what you can do!")
        else:
            db.session.rollback()
            resp.message("We couldn't sign you up, try again.")
    else:
        return_string = process_message(body, member)
        print("Return_string filled.")
        resp.message(return_string)
        
    return str(resp)

def process_message(message, member):
    message = message.split(" ", 1)

    command = message[0].lower()
    try:
        prayer_content = message[1]
    except IndexError:
        prayer_content = ""

    if command == "pray":
        return process_prayer(prayer_content, member)
    elif command == "urgent":
        return process_prayer(prayer_content, member, True)
    elif command == "update":
        return update_prayer(prayer_content, member)
    elif command == "unsubscribe":
        return unsubscribe(prayer_content, member)
    elif command == "subscribe":
        return subscribe(prayer_content, member)
    elif command == "commands":
        return show_commands()
    else:
        return "Command not found. Reply 'commands' for a list of commands."

def process_prayer(prayer_content, member, urgent=False):
    if len(prayer_content) > 2:
        prayer_content = profanity.censor(prayer_content)
        new_prayer = Prayer(prayer_content, member, None)
        db.session.add(new_prayer)
        db.session.flush()
        if new_prayer.id: 
            if urgent:
                if not add_to_groupme(prayer_content):
                    db.session.rollback()
                    return "Couldn't add your prayer, try non-urgent."
            db.session.commit()
            add_to_spreadsheet(prayer_content)
            return "Your prayer was received!"
        else:
            db.session.rollback()
            return "Your prayer didn't work, try again."
    else:
        return "Your prayer wasn't long enough."

def update_prayer(update_content, member):
    update_content = update_content.split(" ", 1)

    prayer_id = int(update_content[0].lower())
    try:
        update_content = update_content[1]
    except IndexError:
        return "Update not long enough, try again!"

    if isinstance(prayer_id, int) and len(update_content) > 2:
        prayer = Prayer.query.filter_by(id=prayer_id, member_id=member.id).first()
        if prayer.id:
            prayer.update = update_content
            db.session.commit()
            send_update.delay(prayer_id)
            return "Prayer updated successfully!"
        else:
            return "Prayer not found, try again!"

def unsubscribe(option, member):
    if option == "digest":
        member.subscribe_digest = False
        db.session.commit()
        return "Successfully unsubscribed from the weekly digest."
    elif option == "update":
        member.subscribe_prayed = False
        db.session.commit()
        return "Successfully unsubscribed from prayer updates."
    else:
        return "Unsubscribe option not found. Use either 'digest' to unsubscribe from the weekly digest or 'update' to unsubscribe from prayer updates from others."

def subscribe(option, member):
    if option == "digest":
        member.subscribe_digest = True
        db.session.commit()
        return "Successfully subscribed to the weekly digest."
    elif option == "update":
        member.subscribe_prayed = True
        db.session.commit()
        return "Successfully subscribed to prayer updates."
    else:
        return "Subscribe option not found. Use either 'digest' to subscribe to the weekly digest or 'update' to subscribe to prayer updates from others."

def show_commands():
    return "Available List of Commands\n\n" + \
    "'pray [prayer here]': Submit a prayer request\n" + \
    "'urgent [prayer here]': Submit a prayer that will be looked at immediately\n" + \
    "'update [prayer number] [update here]': Update people about an answered prayer\n" + \
    "'subscribe [digest|update]': Get a weekly digest or updates on prayers you have prayed for\n" + \
    "'unsubscribe [digest|update]': Discontinue getting a weekly digest or updates on prayers\n" + \
    "\nMore detailed information is available at: http://pray-link.com/..."
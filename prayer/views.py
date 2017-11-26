from flask import request, render_template, jsonify
from prayer_bot_flask import app
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from prayer_bot_flask import db
from profanity import profanity 
from prayer.models import Prayer
from member.models import Member
from utils.spreadsheet_util import add_to_spreadsheet
from utils.groupme_util import add_to_groupme

account_sid = app.config["TEST_ACCOUNT_SID"]
auth_token = app.config["TEST_AUTH_TOKEN"]

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
            resp.message("Welcome to Central Baptist Youth Ministry's prayer request program. Text 'pray [prayer here]' or 'commands' to learn what you can do!")
        else:
            db.session.rollback()
            resp.message("We couldn't sign you up, try again.")
    else:
        return_string = process_message(body, member)
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
            return "Prayer updated successfully!"
        else:
            return "Prayer not found, try again!"

    
        




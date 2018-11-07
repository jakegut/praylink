from flask import request, render_template, jsonify, session, redirect, url_for, flash, make_response
from praylink import app, client, db
from praylink.tasks import send_update
from praylink.member.models import Member
from praylink.prayer.models import Prayer
from praylink.member.decorators import login_required
from praylink.member.form import PhoneField, ValidateNumberForm, PasswordForm, LoginForm, SettingsForm, EditPrayer, AddPrayer
from praylink.group.models import Group
import bcrypt
from random import randint
from profanity import profanity
from praylink.utils.spreadsheet_util import add_to_spreadsheet
from praylink.utils.groupme_util import add_to_groupme

@app.route('/about')
def about():
    return render_template('member/about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = PhoneField()
    error = None

    if form.validate_on_submit():
        phone_number = "+1" + form.phone_number.data.replace('-','')
        member = Member.query.filter_by(phone_number=phone_number).first()

        if member is None:
            member = Member(phone_number)
            if Member.query.count()  == 0:
                member.is_admin = True
            db.session.add(member)
            db.session.flush()

        if member.id and not member.password:
            session['member_id'] = member.id
            if Group.query.count() == 0:
                db.session.commit()
                session['verified'] = True
                return redirect(url_for('signup'))
            member_token = randint(111111, 999999)
            member.token = member_token
            db.session.commit()
            client.messages.create(
                to=phone_number,
                from_=app.config['TWILIO_NUMBER'],
                body="Signup using this token: {}".format(member_token)
            )
            return redirect(url_for('validate'))
        elif member.id and member.password:
            print(member.id)
            error = "Already have a password"
            

    return render_template('member/register.html', form=form, error=error)

@app.route('/verify', methods=['GET', 'POST'])
def validate():
    form = ValidateNumberForm()
    error = None
    
    if 'member_id' in session:
        member_id = session["member_id"]
    else:
        return redirect(url_for('register'))

    if form.validate_on_submit():
        member = Member.query.filter_by(id=session['member_id']).first()

        if member is None:
            return "How did you get here?"
        elif member.token is None:
            return "wtf"

        if form.code.data == member.token:
            member.token = None
            db.session.commit()
            session['verified'] = True
            return redirect(url_for('signup'))
        else:
            return "Wrong code"

    return render_template('member/validate.html', form=form, error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = PasswordForm()
    error = None

    if 'verified' in session:
        if session['verified'] == False:
            return redirect(url_for('register'))

    if 'member_id' in session:
        member_id = session['member_id']
    else:
        return redirect(url_for('register'))

    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        member = Member.query.filter_by(id=member_id).first()

        if member is None:
            return redirect(url_for('register'))
        elif member.password:
            return redirect(url_for('login'))
        else:
            member.password = hashed_password
            db.session.commit()
            session.pop('verified', None)
            session.pop('member_id', None)
            return redirect(url_for('login'))

    return render_template('member/signup.html', form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    
    if form.validate_on_submit():
        phone_number = "+1" + form.phone_number.data.replace('-','')
        member = Member.query.filter_by(phone_number=phone_number).first()

        if member:
            if bcrypt.hashpw(form.password.data, member.password) == member.password:
                session['member_id'] = member.id
                session['is_admin'] = member.is_admin
                print ("Member: {}; is_admin: {}".format(phone_number, member.is_admin))
                if Group.query.count() == 0:
                    return redirect(url_for('new_group'))
                return redirect(url_for('index'))
            else:
                error = "Incorrect phone number or password"
        else:
            error = "Incorrect phone number or password"

    return render_template('member/login.html', form=form, error=error)

@app.route('/logout')
def logout():
    session.pop('member_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    member_id = session['member_id']

    member = Member.query.filter_by(id=member_id).first()
    prayed_for = member.prayed_for
    prayers = member.prayers.all()
    return render_template('member/dashboard.html', prayers=prayers, prayed_for=prayed_for)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_prayer():
    member_id = session['member_id']
    member = Member.query.filter_by(id=member_id).first()
    form = AddPrayer()

    if form.validate_on_submit():
        content = form.content.data
        urgent = 'urgent' in request.form
        if len(content) > 2:
            new_prayer = Prayer(content, member, None)
            db.session.add(new_prayer)
            db.session.flush()
            if new_prayer.id: 
                if urgent:
                    if not add_to_groupme(content):
                        db.session.rollback()
                        flash("Couldn't add your prayer, try non-urgent.")
                db.session.commit()
                add_to_spreadsheet(content)
                flash("Your prayer was added!")
                return redirect(url_for('dashboard'))
            else:
                db.session.rollback()
                flash("Your prayer didn't work, try again.")
        else:
            flash("Your prayer wasn't long enough.")

    return render_template("member/add_prayer.html", form=form)


@app.route('/edit/<int:prayer_id>', methods=['GET', 'POST'])
@login_required
def edit_prayer(prayer_id):
    member_id = session['member_id']
    prayer = Prayer.query.filter_by(id=prayer_id, member_id=member_id).first()
    form = EditPrayer()
    if prayer:
        if form.validate_on_submit():
            prayer.content = form.content.data
            previous_update = prayer.update
            if form.update.data != 'None':
                prayer.update = form.update.data
            db.session.commit()
            if previous_update != prayer.update:
                send_update.delay(prayer.id)
            flash("Prayer updated sucessfully!")
            return redirect(url_for('dashboard'))

        return render_template("member/edit_prayer.html", form=form, prayer=prayer)
    else:
        flash('Prayer not found.')
        return redirect(url_for('dashboard'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    member_id = session['member_id']

    member = Member.query.filter_by(id=member_id).first()

    if request.method == "POST":
        sub_digest = 'sub_digest' in request.form
        sub_update = 'sub_update' in request.form

        if sub_digest:
            member.subscribe_digest = True
        else:
            member.subscribe_digest = False

        if sub_update:
            member.subscribe_prayed = True
        else:
            member.subscribe_prayed = False

        db.session.commit()
        flash("Successfully Updated!")

    return render_template('member/settings.html', member=member)

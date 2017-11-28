from flask import request, render_template, jsonify, session, redirect, url_for, flash, make_response
from prayer_bot_flask import app, client, db
from secrets import randbelow
from member.models import Member
from prayer.models import Prayer
from member.decorators import admin_required
from member.form import PhoneField, ValidateNumberForm, PasswordForm, LoginForm, EditPrayer
import bcrypt

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = PhoneField()
    error = None

    if form.validate_on_submit():
        phone_number = "+1" + form.phone_number.data.replace('-','')
        member = Member.query.filter_by(phone_number=phone_number).first()

        if member is None:
            return "No phone number, you need to use the service first"
        elif member.id and not member.password:
            session['member_id'] = member.id
            member_token = randbelow(999999)
            member.token = member_token
            db.session.commit()
            client.messages.create(
                to=phone_number,
                from_=app.config['TWILIO_NUMBER'],
                body="Signup using this token: {}".format(member_token)
            )
            return redirect(url_for('validate'))
        elif member.id and member.password:
            return "Already have a password"
            

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
                return redirect(url_for('index'))
            else:
                error = "Incorrect phone number or password"
        else:
            error = "Incorrect phone number or password"

    return render_template('member/login.html', form=form, error=error)

@app.route('/logout')
def logout():
    if 'member_id' or 'is_admin' in session:
        session.pop('member_id', None)
        session.pop('is_admin', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin():
    prayers = Prayer.query.order_by(Prayer.publish_date.desc()).all()
    return render_template("member/admin/index.html", prayers=prayers)

@app.route('/admin/edit/<int:prayer_id>', methods=['GET', 'POST'])
@admin_required
def edit_prayer(prayer_id):
    prayer = Prayer.query.filter_by(id=prayer_id).first_or_404()
    form = EditPrayer()

    if form.validate_on_submit():
        prayer.content = form.content.data
        if form.update.data:
            prayer.update = form.update.data
        db.session.commit()
        flash("Prayer updated sucessfully!")
        return redirect(url_for('admin'))

    return render_template("member/admin/edit_prayer.html", form=form, prayer=prayer)

@app.route('/admin/delete/<int:prayer_id>', methods=['POST'])
@admin_required
def delete_prayer(prayer_id):
    prayer = Prayer.query.filter_by(id=prayer_id).first()
    db.session.delete(prayer)
    try:
        db.session.commit()
        return jsonify({"message": "Prayer deleted successfully", "prayer_id": prayer_id})
    except:
        db.session.rollback()
        return make_resonse(jsonify({"message": "Prayer was not deleted", "prayer_id": prayer_id}), 500)



    
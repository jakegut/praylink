from flask import request, render_template, redirect, url_for, flash
from praylink import app, client, db
from praylink.group.models import Group
from praylink.group.form import NewGroupForm
from praylink.member.decorators import admin_required
from praylink.utils.twilio_util import send_twilio_test
from praylink.utils.groupme_util import create_group_bot

@app.route("/newgroup", methods=['GET', 'POST'])
@admin_required
def new_group():
    if Group.query.count() != 0:
        return redirect(url_for('index'))

    form = NewGroupForm()
    error = None

    if form.validate_on_submit():
        group = Group(form.group_name.data)
        db.session.add(group)
        db.session.flush()

        if group.id:
            group.twilio_number = form.phone_number.data
            group.twilio_sid = form.twilio_sid.data
            group.twilio_token = form.twilio_token.data
            group.groupme_token = form.groupme_token.data
            db.session.commit()
            send_twilio_test(group)
            create_group_bot(group)
            return redirect(url_for('index'))
        else:
            error = "Couldn't create group, try again."

    return render_template('group/add.html', form=form, error=error)

@app.route("/editgroup", methods=['GET', 'POST'])
@admin_required
def edit_group():
    if Group.query.count() == 0:
        return redirect(url_for('index'))

    group = Group.query.first()

    form = NewGroupForm()
    error = None

    if form.validate_on_submit():
        new_token = False
        if group.id:
            group.title = form.group_name.data
            group.twilio_number = form.phone_number.data
            group.twilio_sid = form.twilio_sid.data
            group.twilio_token = form.twilio_token.data
            if group.groupme_token != form.groupme_token.data:
                group.groupme_token = form.groupme_token.data
                new_token = True
            db.session.commit()
            send_twilio_test(group)
            create_group_bot(group.id, new_token)
            flash("Changes were successful!")
            return redirect(url_for('index'))
        else:
            error = "Couldn't edit group, try again."

    return render_template('group/edit.html', form=form, group=group, error=error)
        
from flask import Flask, Blueprint, render_template, session, flash, redirect, url_for, g, make_response, jsonify
from praylink import db
from praylink.member.models import Member
from praylink.prayer.models import Prayer
from praylink.admin.form import EditPrayer

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.before_request
def admin_required():
    if session.get('is_admin') is None:
        return redirect(url_for('login'))

@admin_blueprint.route('/')
def index():
    prayers = Prayer.query.order_by(Prayer.publish_date.desc()).all()
    return render_template("admin/index.html", prayers=prayers)

@admin_blueprint.route('/edit/<int:prayer_id>', methods=['GET', 'POST'])
def edit_prayer(prayer_id):
    prayer = Prayer.query.filter_by(id=prayer_id).first_or_404()
    form = EditPrayer()

    if form.validate_on_submit():
        prayer.content = form.content.data
        if form.update.data:
            prayer.update = form.update.data
        db.session.commit()
        flash("Prayer updated sucessfully!")
        return redirect(url_for('admin.index'))

    return render_template("admin/edit_prayer.html", form=form, prayer=prayer)

@admin_blueprint.route('/delete/<int:prayer_id>', methods=['POST'])
def delete_prayer(prayer_id):
    prayer = Prayer.query.filter_by(id=prayer_id).first()
    db.session.delete(prayer)
    try:
        db.session.commit()
        return jsonify({"message": "Prayer deleted successfully", "prayer_id": prayer_id})
    except:
        db.session.rollback()
        return make_response(jsonify({"message": "Prayer was not deleted", "prayer_id": prayer_id}), 500)
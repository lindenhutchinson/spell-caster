from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.spell import Spell

from app.db.db import db

from app.forms import SpellForm


def create_spell():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    form = SpellForm()

    if form.is_submitted():
        spell = Spell(form.name.data, form.level.data, form.cast_time.data, form.concentration.data, form.ritual.data, form.spell_range.data, form.components.data, form.duration.data, form.school.data, form.info.data, form.from_book.data, form.is_bard.data, form.is_cleric.data, form.is_druid.data, form.is_paladin.data, form.is_ranger.data, form.is_sorcerer.data, form.is_warlock.data, form.is_wizard.data)
        db.session.add(spell)
        db.session.commit()

        flash("Created spell!")
        return redirect(url_for('index'))

    return render_template('form.html', form=form, title="Create Spell")

def view_spell():
    default = Spell.query.first()
    if default is None:
        flash("Please create a spell!")
        return redirect(url_for('create_spell'))

    spell = Spell.query.get(request.args.get('id', default = default.id, type = int))

    return render_template('spell.html', spell=spell, title=spell.name)

from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class

from app.db.db import db

from app.forms import CharacterForm
from app.forms import PickCharacterForm


def show():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    char = Character.query.get(session['char_id'])

    form = PickCharacterForm()

    form.character.choices = [(g.id, g.name) for g in current_user.characters]

    if form.is_submitted():
        session['char_id'] = form.character.data
        return redirect(url_for('show'))

    return render_template('char.html', char=char, form=form, title=char.name)



def create():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))
    form = CharacterForm()

    form.class_id.choices = [(g.id, g.name) for g in _Class.query.order_by('name')]

    if form.is_submitted():
        char = Character(form.name.data, form.race.data, form.level.data, form.saving_throw.data, form.ability_score.data,current_user, form.class_id.data)
        db.session.add(char)
        db.session.commit()
        session['char_id'] = char.id
        flash("Created character!")
        return redirect(url_for('show'))

    return render_template('form.html', form=form, title="Create Character")
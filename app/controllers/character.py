from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class

from app.db.db import db

from app.forms import CharacterForm
from app.forms import PickCharacterForm


def view():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    if current_user.characters.count() == 0:
        flash("Please create a character first!")
        return redirect(url_for('create'))


    char = current_user.characters.filter_by(id=session['char_id']).first()

    if not char:
        char = current_user.characters.first()

    form = PickCharacterForm()

    form.character.choices = [(g.id, g.name) for g in current_user.characters]

    if form.is_submitted():
        session['char_id'] = form.character.data
        return redirect(url_for('view'))

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
        return redirect(url_for('view'))

    return render_template('form.html', form=form, title="Create Character")

def edit():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    if not int(session['char_id']) in [c.id for c in current_user.characters]:
        flash("Please select a character first!")
        return redirect(url_for('view'))

    char = current_user.characters.filter_by(id=session['char_id']).first()

    form = CharacterForm()

    form.class_id.choices = [(g.id, g.name) for g in _Class.query.order_by('name')]
 
    form.name.data = char.name
    form.race.data = char.race
    form.level.data = char.level
    form.saving_throw.data = char.saving_throw
    form.ability_score.data = char.ability_score
    form.class_id.data = char.class_id

    if form.validate_on_submit():
        char.name = form.name.data
        char.race = form.race.data
        char.level = form.level.data
        char.saving_throw = form.saving_throw.data
        char.ability_score = form.ability_score.data
        char.class_id = form.class_id.data
        db.session.add(char)
        db.session.commit()
        flash("Updated character!")
        return redirect(url_for('view'))

    return render_template('form.html', form=form, title="Edit Character")

def delete():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    if not session['char_id']:
        flash("Please select a character first!")
        return redirect(url_for('view'))

    current_user.characters.filter_by(id=session['char_id']).delete()
    db.session.commit()
    flash("Character deleted!")
    return redirect(url_for('view'))
    
from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class

from app.db.db import db

from app.forms import CharacterForm
from app.forms import PickCharacterForm
from app.utils.character_helpers import *
from app.utils.model_helpers import *



def view_char():
    if not is_user_logged_in():
        return redirect(url_for('login'))

    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))
        
    if not is_char_id_set():
        session['char_id'] = get_default_char_id()
        print("setting default id")

    char = get_current_char()

    if request.method == 'GET':
        form = PickCharacterForm(formdata=MultiDict({'character': char.id}))
    else:
        form = PickCharacterForm()

    form.character.choices = get_select_characters('name')

    if form.is_submitted():
        session['char_id'] = form.character.data
        return redirect(url_for('view_char'))

    return render_template('char.html', char=char, form=form, title=char.name)



def create_char():
    if not is_user_logged_in():
        return redirect(url_for('login'))

    form = CharacterForm()

    form.class_id.choices = get_select_choices(_Class, 'name')

    if form.is_submitted():
        char = Character(form.name.data, form.race.data, form.level.data, form.saving_throw.data, form.ability_score.data,current_user, form.class_id.data)
        insert_obj(char, "character")
        session['char_id'] = char.id
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Create Character")

def edit_char():
    if not is_user_logged_in():
        return redirect(url_for('login'))

    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))
        
    if not is_char_id_set():
        flash("Please select a character first!")  
        return redirect(url_for('view_char'))

    char = get_current_char()

    if request.method == 'GET':
        form = CharacterForm(formdata=MultiDict({
            'name': char.name,
            'race': char.race,
            'level': char.level,
            'saving_throw': char.saving_throw,
            'ability_score': char.ability_score,
            'class_id': char.class_id
        }))
    else:
        form = CharacterForm()

    form.class_id.choices = get_select_choices(_Class, 'name')

    if form.is_submitted():
        char.name = form.name.data
        char.race = form.race.data
        char.level = form.level.data
        char.saving_throw = form.saving_throw.data
        char.ability_score = form.ability_score.data
        char.class_id = form.class_id.data
        db.session.commit()
        flash("Updated character!")
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Edit Character")

def delete_char():
    if not is_user_logged_in():
        return redirect(url_for('login'))
        
    if not is_char_id_set():
        flash("Please select a character first!")  
        return redirect(url_for('view_char'))

    delete_current_char()
    flash("Character deleted!")

    if user_has_characters():
        session['char_id'] = get_default_char_id()
        return redirect(url_for('view_char'))
    else:
        return redirect(url_for('create_char'))

    
from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.spell import Spell
from app.models.spellbook import Spellbook

from app.db.db import db

from app.forms import SpellForm, PickSpellForm, PickClassForm

from app.utils.character_helpers import *
from app.utils.model_helpers import *
from app.utils.special_helpers import get_filtered_spells
from app.tables.spell_table import SpellTable

def learn_spell():
    char_id = session['char_id']
    spell_id = request.json['spell_id']
    spell = get_model(Spell, spell_id)
    if kw_get_model(Spellbook, char_id=char_id, spell=spell):
        kw_delete_model(Spellbook, char_id=char_id, spell=spell)
        return "Deleted Spellbook"
    else:
        sb = Spellbook(char_id, spell)
        insert_model(sb)
        return "Added Spellbook"

def learn_spells():
    # check user is authenticated
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    # check user has characters
    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))
        
    # check user has a selected character
    if not is_char_id_set():
        flash("Please select a character first!")  
        return redirect(url_for('view_char'))

    char = get_model(Character, session['char_id'])

    # get the url parameter
    filt = request.args.get('filter', default='', type=str)
    spells = get_filtered_spells(filt)
    if not spells:
        flash("No spells found!")
        return redirect(url_for('create_spell'))


    # intialize the Class form
    classForm = PickClassForm()
    # If we have a class object, that means the filter is valid
    _class = kw_get_model(_Class, name=filt)
    if _class:
        if request.method == 'GET':
            # If we have a valid filter and we aren't submitting a form, show the class name as the selected class
            classForm = PickClassForm(formdata=MultiDict({'class_id': _class.id}))
    # If we don't have a valid filter and we aren't submitting a form, show 'All' as the selected class
    elif request.method == 'GET':
        classForm = PickClassForm(formdata=MultiDict({'class_id': 0}))
    # Add the option for 'All' into the select choices
    classForm.class_id.choices = [(0, 'All')]
    # Combine the class choices
    classForm.class_id.choices = classForm.class_id.choices + get_select_choices(_Class, 'name')
    if classForm.is_submitted():
        if classForm.class_id.data == '0':
            return redirect(url_for('learn_spells', filter='All'))
        else:
            return redirect(url_for('learn_spells', filter=get_model(_Class, classForm.class_id.data).name))

    spellbook = get_all_char_child(Spellbook, 'id')
    ids = []
    for sb in spellbook:
        ids.append(sb.spell.id)

    return render_template('learn_spells.html', char=char, classForm=classForm, spellbook=ids, spells=spells, title="Spells")



def delete_spell():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    spell = get_model(Spell, request.args.get('id', type=int))
    if not spell:
        flash("Couldn't find that spell!")
        return redirect(url_for('view_spell'))

    delete_model(spell)

    flash("Spell deleted!")
    return redirect(url_for('view_spell')) if get_default(Spell) else redirect(url_for('index'))
from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.spell import Spell
from app.models.slots import Slots
from app.models.spellbook import Spellbook
from app.db.db import db

from app.forms import CharacterForm
from app.forms import PickCharacterForm
from app.utils.character_helpers import *
from app.utils.model_helpers import *


def view_char():
    # check user is authenticated
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    # check user has characters
    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))

    # check user has selected a character  
    if not is_char_id_set():
        session['char_id'] = get_default_char_id()

    # char = get_current_char()
    char = get_model(Character, session['char_id'])

    # get the character's spell slots 
    slots = get_char_child_default(Slots)
    
    # the SelectField should show the currently selected character
    if request.method == 'GET':
        form = PickCharacterForm(formdata=MultiDict({'character': char.id}))
    else:
        form = PickCharacterForm()

    form.character.choices = get_select_characters('name')

    if form.is_submitted():
        session['char_id'] = form.character.data
        return redirect(url_for('view_char'))

    spellbooks = get_all_char_child(Spellbook, 'id')
    spellbook = get_all_char_child(Spellbook, 'id')
    prep_spells = []

    
    for sb in spellbook:
        if sb.prepared:
            prep_spells.append(sb.spell)

    

    if len(prep_spells) == 0:
        flash("Try preparing some spells!")

    lvls = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    
    for s in prep_spells:
        lvls[s.level].append(s)
    return render_template('char.html', lvls=lvls, slots=slots,char=char, form=form, title=char.name)



def create_char():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    form = CharacterForm()

    form.class_id.choices = get_select_choices(_Class, 'name')

    if form.is_submitted():
        char = insert_form(Character, form, current_user)

        if get_model(_Class, char.class_id).name == 'Druid':
            for s in kw_get_models(Spell, is_druid=1):
                if int(s.level) == 0:
                    continue
                insert_model(Spellbook(char.id, s))
        elif get_model(_Class, char.class_id).name == 'Cleric':
            for s in kw_get_models(Spell, is_cleric=1): 
                if int(s.level) == 0:
                    continue
                insert_model(Spellbook(char.id, s))

        # If a character is created, we should create some slots for them as well!
        insert_model(Slots(char))
        flash("Created a character!")
        session['char_id'] = char.id
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Create Character")

def edit_char():
    if not current_user.is_authenticated:
        flash("Please login first!")
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
            'casting_ability': char.casting_ability,
            'ability_score': char.ability_score,
            'class_id': char.class_id
        }))
    else:
        form = CharacterForm()

    form.class_id.choices = get_select_choices(_Class, 'name')

    if form.is_submitted():
        # If a character's level is changed, then we should update their slots
        slot_work=False
        if int(form.level.data) != int(char.level):
            slot_work=True
        update_form(char, form)
        if slot_work:
            kw_delete_model(Slots, char_id=char.id)
            insert_model(Slots(get_current_char()))
        flash("Updated character!")
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Edit Character")

def delete_char():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    if not is_char_id_set():
        flash("Please select a character first!")  
        return redirect(url_for('view_char'))

    char = get_model(Character, session['char_id'])
    delete_model(char)
    flash("Deleted character!")
    if user_has_characters():
        session['char_id'] = get_default_char_id()
        return redirect(url_for('view_char'))
    else:
        return redirect(url_for('view_all_spells'))

    
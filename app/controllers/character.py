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
from app.models.stats import Stats
from app.models.action import Action
from app.db.db import db

from app.forms import CharacterForm
from app.forms import PickCharacterForm
from app.forms import ResetSlotsForm
from app.forms import StatsForm
from app.utils.character_helpers import *
from app.utils.model_helpers import *
from app.utils.special_helpers import reset_slots, get_slots, get_prof_bonus

# needs updating


def change_slot_val():
    char_id = session['char_id']
    lvl = request.json['slot_lvl']
    res = request.json['slot_res']
    slot = kw_get_model(Slots, char_id=char_id)
    kw_update_model(slot, {lvl: res}, char_id=char_id)
    return "Updated a {} slot!".format(lvl)


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

    # get the current character
    char = get_model(Character, session['char_id'])

    # the SelectField should show the currently selected character
    if request.method == 'GET':
        form1 = PickCharacterForm(character=char.id, prefix="form1")
    else:
        form1 = PickCharacterForm(prefix="form1")

    form1.character.choices = get_select_characters('name')

    if form1.is_submitted() and form1.submit.data:
        session['char_id'] = form1.character.data
        return redirect(url_for('view_char'))

    form2 = ResetSlotsForm(prefix="form2")
    if form2.is_submitted() and form2.submit.data:
        reset_slots(char)
        return redirect(url_for('view_char'))

    # get all spellbooks owned by the character
    spellbooks = get_all_char_child(Spellbook, 'id')
    prep_spells = []
    unprep_spells = []
    # curate a list of prepared spellbooks
    for sb in spellbooks:
        if sb.prepared:
            prep_spells.append(sb.spell)
        else:
            unprep_spells.append(sb.spell)

    # Split prepared spells by level so they can be separated on the page
    lvls = {0: [], 1: [], 2: [], 3: [], 4: [],
            5: [], 6: [], 7: [], 8: [], 9: []}

    spaces = get_slots(char.level)
    for s in prep_spells:
        if s.level > len(spaces):
            continue
        if spaces[s.level-1] == 0 and s.level != 0:
            continue
        lvls[s.level].append(s)

    for s in unprep_spells:
        if s.level > len(spaces):
            continue
        if spaces[s.level-1] == 0 and s.level != 0:
            continue
        lvls[s.level].append(s)


    p_spells = [s for s in kw_get_models(Spellbook, char_id=char.id, prepared=1) if s.spell.level > 0]
    p_lvls = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    
    for p in p_spells:
        p_lvls[p.spell.level].append(p.spell)
    
    total = len(p_spells)

    # get the character's spell slots
    slots = get_char_child_default(Slots)
    # put the slot info into an easy to access array that can be accessed by the page
    slots = [slots.lvl_1, slots.lvl_2, slots.lvl_3, slots.lvl_4,
             slots.lvl_5, slots.lvl_6, slots.lvl_7, slots.lvl_8, slots.lvl_9]

    char.prof_bonus = get_prof_bonus(char.level)

    stats = get_char_child_default(Stats)
    actions = get_all_char_child(Action, 'name')
    prep_spells = [s.id for s in prep_spells]
    unprep_spells = [s.id for s in unprep_spells]
    return render_template(
        'char.html', 
        p_lvls=p_lvls, 
        total=total, 
        prep_spells=prep_spells, 
        unprep_spells=unprep_spells, 
        actions=actions, 
        stats=stats, 
        lvls=lvls, 
        slots=slots, 
        char=char, 
        resetSlotsForm=form2, 
        form=form1, 
        title=char.name
    )


def edit_stats():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))

    if not session['char_id']:
        flash("Please select a character first!")
        return redirect(url_for('view_char'))

    char = get_model(Character, session['char_id'])
    stats = get_char_child_default(Stats)
    if request.method == 'GET':
        form = StatsForm(formdata=MultiDict({
            'wis_': stats.wis_,
            'str_': stats.str_,
            'int_': stats.int_,
            'dex_': stats.dex_,
            'con_': stats.con_,
            'chr_': stats.chr_,
            'ac': stats.ac,
            'max_hp': stats.max_hp,
            'spell_save': stats.spell_save if stats.spell_save else 0,
            'spell_attack': stats.spell_attack if stats.spell_attack else 0,
        }))
    else:
        form = StatsForm()

    if form.validate_on_submit():
        kw_update_form(stats, form, char_id=char.id)
        # f_stats = form.stats.data
        # f_stats.pop('csrf_token')
        # stat = kw_get_model(Stats, char_id=char.id)
        # kw_update_model(stat, f_stats, char_id=char.id)
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Edit Stats")
    

def create_stats():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))

    if not session['char_id']:
        flash("Please select a character first!")
        return redirect(url_for('view_char'))

    char = get_model(Character, session['char_id'])
    form = StatsForm()

    if form.is_submitted():
        insert_form(Stats, form, character=char)
        flash("Added stats to character!")
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Create Stats")
        # stats = form.stats.data
        # stats.pop('csrf_token')
        # delattr(form, 'stats')
        # if get_char_child_default(Stats):
        #     stats = kw_get_model(Stats, char_id=char.id)
        #     kw_update_model(stats, *stats.values(), char_id=char.id)
        # else:
        #     stats = Stats(char, *stats.values())
        #     insert_model(stats)


def create_char():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    form = CharacterForm()

    form.class_id.choices = get_select_choices(_Class, 'name')
    # form.race_id.choices = get_select_choices(Race, 'name')

    if form.is_submitted():
        char = insert_form(Character, form, user=current_user)
        _class = get_model(_Class, char.class_id)
        if _class.name == 'Druid':
            for sc in _class.spells:
                s = sc.spell
                if int(s.level) == 0:
                    continue
                    
                insert_model(Spellbook(char.id, s))
        elif _class.name == 'Cleric':
            for sc in _class.spells:
                s = sc.spell
                if int(s.level) == 0:
                    continue

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

    # if not is_char_id_set():
    if not session['char_id']:
        flash("Please select a character first!")
        return redirect(url_for('view_char'))

    char = get_current_char()
    if request.method == 'GET':
        form = CharacterForm(formdata=MultiDict({
            'name': char.name,
            'level': char.level,
            'class_id': char.class_id,
            'is_npc': char.is_npc,
        }))
    else:
        form = CharacterForm()

    form.class_id.choices = get_select_choices(_Class, 'name')

    if form.is_submitted():
        # If a character's level is changed, then we should update their slots
        # need to check this before the form has been updated
        slot_work = True if int(form.level.data) != int(char.level) else False

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

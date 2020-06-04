from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.spell import Spell

from app.db.db import db

from app.forms import SpellForm, PickSpellForm, PickClassForm

from app.utils.model_helpers import *
from app.tables.spell_table import SpellTable


def create_spell():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    form = SpellForm()

    if form.validate_on_submit():
        spell = insert_form(Spell, form)
        flash("Created spell!")
        return redirect(url_for('view_spell', id=spell.id))

    return render_template('spell_form.html', form=form, title="Create Spell")


def view_spell():
    default = get_default(Spell)
    if default is None:
        flash("No spells found!")
        return redirect(url_for('create_spell'))

    spell = get_model(Spell, request.args.get(
        'id', default=default.id, type=int))
    if not spell:
        flash("Couldn't find that spell!")
        return redirect(url_for('index'))

    # if the form isn't being submitted, the SelectField should show the currently selected spell
    if request.method == 'GET':
        form = PickSpellForm(formdata=MultiDict({'spell_ids': spell.id}))
    else:
        form = PickSpellForm()

    spells = get_all_models(Spell)

    # fill the SelectField with all the spells
    form.spell_ids.choices = get_select_choices(Spell, 'name')

    if form.is_submitted():
        return redirect(url_for('view_spell', id=form.spell_ids.data))

    return render_template('spell.html', form=form, spell=spell, title=spell.name)


def view_all_spells():
    # get the url parameter
    filt = request.args.get('filter', default='', type=str)

    # check if the url parameter is a valid class
    # if it is, get the list of spells that are available to that class
    # otherwise, just get a list of all spells
    if filt == 'Bard':
        spells = get_filtered_models(Spell, is_bard=1)
    elif filt == 'Cleric':
        spells = get_filtered_models(Spell, is_cleric=1)
    elif filt == 'Druid':
        spells = get_filtered_models(Spell, is_druid=1)
    elif filt == 'Paladin':
        spells = get_filtered_models(Spell, is_paladin=1)
    elif filt == 'Ranger':
        spells = get_filtered_models(Spell, is_ranger=1)
    elif filt == 'Sorcerer':
        spells = get_filtered_models(Spell, is_sorcerer=1)
    elif filt == 'Warlock':
        spells = get_filtered_models(Spell, is_warlock=1)
    elif filt == 'Wizard':
        spells = get_filtered_models(Spell, is_wizard=1)
    else:
        spells = get_all_models(Spell)

    # Find the class model associated with the filter
    _class = get_model_by_name(_Class, filt)

    if not spells:
        flash("No spells found!")
        return redirect(url_for('create_spell'))

    table = SpellTable(spells)

    # intialize the Class form
    form = PickClassForm()

    # If we have a class object, that means the filter is valid
    if _class:
        if request.method == 'GET':
            # If we have a valid filter and we aren't submitting a form, show the class name as the selected class
            form = PickClassForm(formdata=MultiDict({'class_id': _class.id}))
    # If we don't have a valid filter and we aren't submitting a form, show 'All' as the selected class
    elif request.method == 'GET':
        form = PickClassForm(formdata=MultiDict({'class_id': 0}))

    # Add the option for 'All' into the select choices
    form.class_id.choices = [(0, 'All')]
    # Combine the class choices
    form.class_id.choices = form.class_id.choices + get_select_choices(_Class, 'name')
    if form.is_submitted():
        if form.class_id.data == '0':
            return redirect(url_for('view_all_spells', filter='All'))
        else:
            return redirect(url_for('view_all_spells', filter=get_model(_Class, form.class_id.data).name))

    return render_template('all_spells.html', form=form, table=table, title="Spells")


def edit_spell():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    spell = get_model(Spell, request.args.get('id', type=int))
    if not spell:
        flash("Couldn't find that spell!")
        return redirect(url_for('view_spell'))

    if request.method == 'GET':
        form = SpellForm(formdata=MultiDict({
            'name': spell.name,
            'level': spell.level,
            'cast_time': spell.cast_time,
            'spell_range': spell.spell_range,
            'components': spell.components,
            'duration': spell.duration,
            'school': spell.school,
            'info': spell.info,
            'scaling': spell.scaling,
            'from_book': spell.from_book,
            'concentration': spell.concentration,
            'is_bard': spell.is_bard,
            'is_cleric': spell.is_cleric,
            'is_druid': spell.is_druid,
            'is_paladin': spell.is_paladin,
            'is_ranger': spell.is_ranger,
            'is_sorcerer': spell.is_sorcerer,
            'is_warlock': spell.is_warlock,
            'is_wizard': spell.is_wizard
        }))

    else:
        form = SpellForm()

    if form.is_submitted():
        update_form(spell, form)

        flash("Updated spell!")
        return redirect(url_for('view_spell', id=spell.id))

    return render_template('spell_form.html', form=form, title="Edit Spell")


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

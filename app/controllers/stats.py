from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user
from werkzeug.datastructures import MultiDict
from app.forms import StatsForm
from app.utils.character_helpers import *
from app.utils.model_helpers import *

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

    if form.validate_on_submit():
        insert_form(Stats, form, character=char)
        flash("Added stats to character!")
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Create Stats")

    
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
        return redirect(url_for('view_char'))

    return render_template('form.html', form=form, title="Edit Stats")



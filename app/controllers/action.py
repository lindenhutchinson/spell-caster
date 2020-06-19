from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.stats import Stats
from app.models.action import Action
from app.db.db import db

from app.forms import ActionForm
from app.forms import PickActionForm
from app.utils.character_helpers import *
from app.utils.model_helpers import *

def change_action_res():
    action_id = request.json['id']
    new_res = int(request.json['res'])
    action = kw_get_model(Action, id=action_id)
    print(action)
    kw_update_model(action, {'res': new_res}, id=action_id)
    return "Updated an action resource!"

def delete_action():
    pass

def edit_action():
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

    default = get_char_child_default(Action)
    if not get_char_child(Action, request.args.get('id', type=int)):
        flash("Couldn't find that action")
        return redirect(url_for('view_action'))

    # get the note selected via url parameter, so long as it is owned by the current character
    action = get_char_child(Action, request.args.get('id',type = int))


    if request.method == 'GET':
        form = ActionForm(formdata=MultiDict({
            'name':action.name,
            'desc':action.desc,
            'max_res':action.max_res
        }))         
    else:
        form = ActionForm()

    if form.validate_on_submit():
        update_form(action, form)
        return redirect(url_for('view_action', id=action.id))

    return render_template('form.html', form=form, action=action, char=char, title='Edit Action')


def view_action():
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

    default = get_char_child_default(Action)
    if not default:
        flash("Please create an action")
        return redirect(url_for('create_action'))

    # get the action selected via url parameter, so long as it is owned by the current character
    action = get_char_child(Action, request.args.get('id', default = default.id, type = int))

    if request.method == 'GET':
        form = PickActionForm(formdata=MultiDict({
            'id': action.id,  
        }))
    else:
        form = PickActionForm()

    actions = get_all_char_child(Action, 'name')
    form.id.choices = [(g.id, g.name) for g in actions]

    
    if form.is_submitted():
        return redirect(url_for('view_action', id=form.id.data))

    return render_template('action.html', form=form, action=action, char=char, title=action.name)

def create_action():
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

    form = ActionForm()

    if form.is_submitted():
        insert_form(Action, form, character=char)
        flash("Created an action!")
        return redirect(url_for('view_action'))

    return render_template('form.html', form=form, title="Create Action")

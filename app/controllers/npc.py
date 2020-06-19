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
from app.db.db import db

from app.utils.character_helpers import *
from app.utils.model_helpers import *
from app.utils.special_helpers import reset_slots, get_slots, get_prof_bonus


def view_npcs():
     # check user is authenticated
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))



    npcs = kw_get_models(Character, is_npc=True, user_id=current_user.id)
    # check user has npcs
    if not npcs:
        flash("Please create an npc first!")
        return redirect(url_for('create_char'))

    return render_template('npc.html', npcs=npcs)

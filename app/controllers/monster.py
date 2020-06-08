from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.note import Note
from app.models.monster import Monster

from app.db.db import db

from app.utils.model_helpers import *




def view_monster():
    if not get_default(Monster):
        flash("Sorry there's nothing there!")
        return redirect(url_for('view_all_spells'))


    monsters = get_all_models(Monster)


    return render_template('monster.html', monsters=monsters, title="Monsters")


    
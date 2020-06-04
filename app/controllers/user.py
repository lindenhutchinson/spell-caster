from flask import render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user
from app.models.user import User
from app.db.db import db

from app.forms import RegisterForm
from app.forms import LoginForm

def register():
    form = RegisterForm()
    if form.is_submitted():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Created user!")
        return redirect(url_for('login'))

    return render_template('form.html', form=form, title="Register")

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        session['char_id'] = 0
        return redirect(url_for('index'))

    return render_template('form.html', form=form, title="Login")

def logout():
    session['char_id'] = 0
    logout_user()
    return redirect(url_for('index'))

'''
    def view_user():
        take a look at controllers/character.py - view_char()
        we won't need most of the checks because the user is required for everything.
        we only need to make sure the user is authenticated 
        But it should give an idea of what controllers are doing

        utils/model_helpers.py will be your friend when working with controllers 
        

    def edit_user():

    view user will need a new 'view' - user.html
    it could show the user name and their number of characters.
    take a look at note.html for reference

    for edit_user, we can use a form to easily create the edit form for a user
    check out forms.py and form.html



'''
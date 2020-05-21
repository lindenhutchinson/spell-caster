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
        return redirect(url_for('index'))

    return render_template('form.html', form=form, title="Login")

def logout():
    session['char_id'] = ''
    logout_user()
    return redirect(url_for('index'))

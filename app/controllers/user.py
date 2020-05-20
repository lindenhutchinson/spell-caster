from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user
from app.models.user import User
from app.db.db import db

from app.forms import SignupForm
from app.forms import LoginForm


def signup():
    form = SignupForm()
    if form.is_submitted():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('login.html', form=form)

def logout():
    logout_user()
    return redirect("/")
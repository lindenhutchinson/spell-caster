from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user

from werkzeug.datastructures import MultiDict

from app.models._class import _Class

from app.db.db import db

from app.forms import ClassForm, PickClassForm


def create_class():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))
    form = ClassForm()

    if form.is_submitted():
        _class = _Class(form.name.data, form.desc.data)
        db.session.add(_class)
        db.session.commit()
        flash("Created class!")
        return redirect(url_for('view_class', id=_class.id))

    return render_template('form.html', form=form, title="Create Class")

def view_class():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))

    default_id = _Class.query.first()
    if default_id is None:
        flash("Please create a class!")
        return redirect(url_for('create_class'))

    _class = _Class.query.get(request.args.get('id', default = default_id.id, type = int))

    if not _class:
        flash("Couldn't find that class!")
        return redirect(url_for('index'))

    if request.method == 'GET':
        form = PickClassForm(formdata=MultiDict({'class_id': _class.id}))
    else:
        form = PickClassForm()

    form.class_id.choices = [(g.id, g.name) for g in _Class.query.all()]

    if form.is_submitted():
        return redirect(url_for('view_class', id=form.class_id.data))

    return render_template('class.html', _class=_class, form=form, title=_class.name)


def edit_class():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))
    
    class_id = request.args.get('id', type = int)
    if not class_id:
        flash("Couldn't find that class!")
        return redirect(url_for('index'))

    _class = _Class.query.get(class_id)

    if request.method == 'GET':
        form = ClassForm(formdata=MultiDict({
            'name': _class.name,
            'desc': _class.desc
        }))
    else:
        form = ClassForm()

    if form.is_submitted():
        _class.name = form.name.data
        _class.desc = form.desc.data
        db.session.commit()

        flash("Updated class!")
        return redirect(url_for('view_class', id=_class.id))

    return render_template('form.html', form=form, title="Edit Class")

def delete_class():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('login'))
    
    class_id = request.args.get('id', type = int)

    if not class_id:
        flash("Couldn't find that class!")
        return redirect(url_for('index'))

    _class = _Class.query.get(class_id)

    if len(_class.characters) > 0:
        flash("Can't delete a class that characters are using!")
        return redirect(url_for('view_class', id=_class.id))

    _class.query.delete()
    db.session.commit()
    flash("Class deleted!")
    return redirect(url_for('view_class'))
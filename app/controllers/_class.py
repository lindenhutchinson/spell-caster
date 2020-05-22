from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user
from werkzeug.datastructures import MultiDict

from app.models._class import _Class

from app.db.db import db

from app.utils.model_helpers import is_user_logged_in, insert_obj, is_obj, get_default, is_default, get_model, get_select_choices

from app.forms import ClassForm, PickClassForm


def create_class():
    if not is_user_logged_in():
        return redirect(url_for('login'))

    form = ClassForm()

    if form.is_submitted():
        _class = _Class(form.name.data, form.desc.data)
        insert_obj(_class, "class")
        return redirect(url_for('view_class', id=_class.id))

    return render_template('form.html', form=form, title="Create Class")

def view_class():
    if not is_user_logged_in():
        return redirect(url_for('login'))

    default = get_default(_Class)

    if not is_default(default, "class"):
        return redirect(url_for('create_class'))

    _class = get_model(_Class, request.args.get('id', default = default.id, type = int))
    if not is_obj(_class, "class"):
        return redirect(url_for('index'))

    if request.method == 'GET':
        form = PickClassForm(formdata=MultiDict({'class_id': _class.id}))
    else:
        form = PickClassForm()

    form.class_id.choices = get_select_choices(_Class, 'name')

    if form.is_submitted():
        return redirect(url_for('view_class', id=form.class_id.data))

    return render_template('class.html', _class=_class, form=form, title=_class.name)


def edit_class():
    if not is_user_logged_in():
        return redirect(url_for('login'))

    default = get_default(_Class)
    if not is_default(default, "class"):
        return redirect(url_for('create_class'))

    _class = get_model(_Class, request.args.get('id', default = default.id, type = int))
    if not is_obj(_class, "class"):
        return redirect(url_for('view_class'))

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
    if not is_user_logged_in():
        return redirect(url_for('login'))
    
    _class = get_model(_Class, request.args.get('id', type = int))
    if not is_obj(_class, "class"):
        return redirect(url_for('view_class'))

    if len(_class.characters) > 0:
        flash("Can't delete a class that characters are using!")
        return redirect(url_for('view_class', id=_class.id))

    _class.query.delete()
    db.session.commit()
    flash("Class deleted!")
    return redirect(url_for('view_class'))
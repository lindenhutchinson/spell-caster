from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.note import Note

from app.db.db import db

from app.forms import NoteForm, PickNoteForm

from app.utils.model_helpers import *
from app.utils.character_helpers import *
from app.utils.note_helpers import *



def create_note():
    if not is_user_logged_in:
        return redirect(url_for('login'))

    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))
        
    if not is_char_id_set():
        flash("Please select a character first!")  
        return redirect(url_for('view_char'))

    char = get_current_char()

    form = NoteForm()

    if form.is_submitted():
        note = Note(form.title.data,form.body.data, char.id)
        insert_obj(note, "note")
        return redirect(url_for('view_note'))

    return render_template('form.html', form=form, title="Create Spell")

def view_note():
    if not is_user_logged_in:
        return redirect(url_for('login'))

    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))
        
    if not is_char_id_set():
        flash("Please select a character first!")  
        return redirect(url_for('view_char'))

    char = get_current_char()

    if not character_has(Note):
        flash("Please create a note first!")
        return redirect(url_for('create_note'))

    default = get_char_child_default(Note)

    if not is_default(default, "note"):
        return redirect(url_for('create_note'))

    note = get_char_child(Note, request.args.get('id', default = default.id, type = int))

    if not is_obj(note, "note"):
        return redirect(url_for('index'))

    if request.method == 'GET':
        form = PickNoteForm(formdata=MultiDict({'note_id': note.id}))
    else:
        form = PickNoteForm()

    notes = get_all_char_child(Note, 'title')
    form.note_id.choices = get_select_notes(notes, 'note')
    
    if form.is_submitted():
        return redirect(url_for('view_note', id=form.note_id.data))

    return render_template('note.html', form=form, note=note, char=char, title=note.title)

def edit_note():
    if not is_user_logged_in:
        return redirect(url_for('login'))

    if not user_has_characters():
        flash("Please create a character first!")
        return redirect(url_for('create_char'))
        
    if not is_char_id_set():
        flash("Please select a character first!")  
        return redirect(url_for('view_char'))

    default = get_char_child_default(Note)

    if not is_default(default, "note"):
        return redirect(url_for('create_note'))

    note = get_char_child(Note, request.args.get('id', default = default.id, type = int))

    if not is_obj(note, "note"):
        return redirect(url_for('view_note'))

    if request.method == 'GET':
        form = NoteForm(formdata=MultiDict({
            'title': note.title,
            'body': note.body
        }))
    else:
        form = NoteForm()

    if form.is_submitted():
        note.title = form.title.data
        note.body = form.body.data
        db.session.commit()

        flash("Updated note!")
        return redirect(url_for('view_note', id=note.id))

    return render_template('form.html', form=form, title="Edit Note")
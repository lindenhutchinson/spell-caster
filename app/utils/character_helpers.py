from flask import session
from flask_login import current_user
from app.db.db import db

# returns boolean
# checks if current user has created any characters
def user_has_characters():
    return False if current_user.characters.count() == 0 else True

# returns boolean
# checks if the session character id is set one of the current user's characters
def is_char_id_set():
    return True if int(session['char_id']) in [c.id for c in current_user.characters] else False

# returns the currently selected character
def get_current_char():
    return current_user.characters.filter_by(id=session['char_id']).first()

def delete_current_char():
    current_user.characters.filter_by(id=session['char_id']).delete()
    db.session.commit()
# returns a character owned by the current user
def get_default_char_id():
    return current_user.characters.first().id

# returns a list of characters, owned by the current user, formatted for a SelectField
def get_select_characters(orderby):
    return [(g.id, g.name) for g in current_user.characters.order_by(orderby)]

# returns boolean
# checks if the currently selected character has created any items of the given model
def character_has(model):
    return False if model.query.filter_by(char_id=session['char_id']).count() == 0 else True

# returns an object of a given model owned by the currently selected character, filtered by id
def get_char_child(model, id):
    return model.query.filter_by(char_id=session['char_id'], id=id).first()

# returns the first object of a given model owned by the currently selected character
def get_char_child_default(model):
    return model.query.filter_by(char_id=session['char_id']).first()

# returns all objects of a given model owned by the currently selected character
def get_all_char_child(model, orderby):
    return model.query.filter_by(char_id=session['char_id']).order_by(orderby).all()
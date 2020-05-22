from flask import session
from flask_login import current_user
from app.db.db import db

# returns boolean
# checks if current user has created any characters
def user_has_characters():
    return current_user.characters.count() != 0


# returns boolean
# checks if the currently selected character has created any items of the given model
def character_has(model):
    return model.query.filter_by(char_id=session['char_id']).count() != 0

# returns boolean
# checks if the session character id is set to one of the current user's characters
def is_char_id_set():
    return True if str(session['char_id']) in [str(c.id) for c in current_user.characters] else False

# returns the currently selected character
def get_current_char():
    return current_user.characters.filter_by(id=session['char_id']).first()

# returns a character owned by the current user
def get_default_char_id():
    return current_user.characters.first().id

# returns a list of characters, owned by the current user, formatted for a SelectField
def get_select_characters(orderby):
    return [(g.id, g.name) for g in current_user.characters.order_by(orderby)]


# returns an object of a given model owned by the currently selected character, filtered by id
def get_char_child(model, id):
    return model.query.filter_by(char_id=session['char_id'], id=id).one()

# returns the first object of a given model owned by the currently selected character
def get_char_child_default(model):
    return model.query.filter_by(char_id=session['char_id']).first()

# returns all objects of a given model owned by the currently selected character
def get_all_char_child(model, orderby):
    return model.query.filter_by(char_id=session['char_id']).order_by(orderby).all()
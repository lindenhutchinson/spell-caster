from flask import flash, session
from flask_login import current_user
from app.db.db import db

# returns Boolean
# checks if the current user is authenticated
def is_user_logged_in():
    if not current_user.is_authenticated:
        flash("Please login first!")
        return False
    
    return True

# inserts a model instance into the database
def insert_obj(obj, obj_name):
    db.session.add(obj)
    db.session.commit()
    flash("Created {}".format(obj_name))

# returns a list of ids and names to be used in a SelectField
def get_select_choices(model, orderby):
    return [(g.id, g.name) for g in model.query.order_by(orderby).all()]

# returns a model instance id
def get_model(model, id):
    return model.query.get(id)

# returns a boolean
# checks if the referenced object exists, updates flash message if not
def is_obj(obj, model_name):
    if not obj:
        flash("Couldn't find that {}!".format(model_name))
        return False

    return True

# returns the first item in a database column
def get_default(model):
    return model.query.first()

# returns a boolean
# checks if the referenced default value exists, updates flash message if not
def is_default(default, model_name):
    if(not default):
        flash("Please create a {}!".format(model_name))
        return False

    return True


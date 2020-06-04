from flask import session
from flask_login import current_user
from app.db.db import db

def set_slot(model,**kwargs):
    model.query.filter_by(char_id=current_user.id).update(**kwargs)
    db.session.commit()


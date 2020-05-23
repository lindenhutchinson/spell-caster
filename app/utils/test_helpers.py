from app.db import db

# inserts a model object into the database
def insert_model(model):
    db.db.session.add(model)
    db.db.session.commit()

# returns a list of ids and names to be used in a SelectField
def get_select_choices(model, orderby):
    return [(g.id, g.name) for g in model.query.order_by(orderby).all()]

# returns a model instance by a given id
def get_model(model, id):
    return model.query.get(id)

# returns the first item in a database column
def get_default(model):
    return model.query.first()

# deletes the referenced model
def delete_model(model):
    model.query.filter_by(id=model.id).delete()
    db.db.session.commit()

from app.db.db import db
import inspect
import string

# inserts a model object into the database
def insert_model(model):
    db.session.add(model)
    db.session.commit()
    return model

# inserts a model object into the database, getting the model values via a passed form
def insert_form(model, form, **kwargs):
    items = {}
    for item in form:
        # print(item.name)
        # if item.data and item is not form.csrf_token and item is not form.submit:
        if item is not form.csrf_token and item is not form.submit:
            items.update({item.name:item.data})

    print(items)
    obj = model(**items, **kwargs)
    db.session.add(obj)
    db.session.commit()

    return obj
   
def insert_seeded_model(model, data, *args):
    obj = model(*data.items(), *args)
    db.session.add(obj)
    db.session.commit()
    
# updates a model object via the values passed in a form
def update_form(obj, form):
    # idk why but removing these two lines makes this break
    inspect.getmembers(obj)
    inspect.getmembers(form)

    updates = {}
    for key in obj.__dict__.keys():
        if hasattr(form, key) and type(form[key].data) is not dict:
            updates.update({key:form[key].data})

    obj.query.filter_by(id=obj.id).update(updates)
    db.session.commit()

def kw_update_form(obj, form, **kwargs):
    # idk why but removing these two lines makes this break
    inspect.getmembers(obj)
    inspect.getmembers(form)

    updates = {}
    for key in obj.__dict__.keys():
        if hasattr(form, key) and type(form[key].data) is not dict:
            updates.update({key:form[key].data})

    obj.query.filter_by(**kwargs).update(updates)
    db.session.commit()

def kw_update_model(obj, updates, **kwargs):
    obj.query.filter_by(**kwargs).update(updates)
    db.session.commit()

def update_model(obj, updates):
    obj.query.filter_by(id=obj.id).update(updates)
    db.session.commit()
# returns a list of ids and names to be used in a SelectField
def get_select_choices(model, orderby):
    return [(g.id, g.name) for g in model.query.order_by(orderby).all()]

# returns a model instance by a given id
def get_model(model, id):
    return model.query.get(id)


def get_all_models(model):
    return model.query.all()

# returns the first item in a database column
def get_default(model):
    return model.query.first()

# deletes the referenced model
def delete_model(model):
    model.query.filter_by(id=model.id).delete()
    db.session.commit()

def kw_delete_model(model, **kwargs):
    model.query.filter_by(**kwargs).delete()
    db.session.commit()

def kw_get_model(model, **kwargs):
    return model.query.filter_by(**kwargs).first()



def kw_get_models(model, **kwargs):
    return model.query.filter_by(**kwargs).all()
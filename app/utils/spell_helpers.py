from app.db.db import db
from app.models._class import _Class
from app.models.spellclass import SpellClass
from app.utils.model_helpers import kw_get_model, kw_get_models, delete_model
import inspect
import string
def insert_spell_form(model, form, **kwargs):
    items = {}
    classes = []
    for item in form:
        # print(item.name)
        # if item.data and item is not form.csrf_token and item is not form.submit:
        if item is not form.csrf_token and item is not form.submit:
            if 'is_' in item.name:
                if item.data:
                    name = item.name.lstrip('is_').capitalize()
                    classes.append(kw_get_model(_Class, name=name))
            else:
                items.update({item.name:item.data})

    print(items)
    spell = model(**items, **kwargs)
    db.session.add(spell)

    for c in classes:
        sc = SpellClass(c, spell)
        db.session.add(sc)

    db.session.commit()
    return spell
 

   
# updates a model object via the values passed in a form
def update_spell_form(obj, form):
    # idk why but removing these two lines makes this break
    inspect.getmembers(obj)
    inspect.getmembers(form)

    updates = {}
    classes = []

    for key in obj.__dict__.keys():
        if hasattr(form, key) and type(form[key].data) is not dict:
            updates.update({key:form[key].data})

    for item in form:
        if item is not form.csrf_token and item is not form.submit:
            if 'is_' in item.name:
                if item.data:
                    name = item.name.lstrip('is_').capitalize()
                    classes.append(kw_get_model(_Class, name=name))

    existing = kw_get_models(SpellClass, spell=obj)
    for e in existing:
        delete_model(e)

    for c in classes:
        sc = SpellClass(c, obj)
        db.session.add(sc)

    obj.query.filter_by(id=obj.id).update(updates)
    db.session.commit()



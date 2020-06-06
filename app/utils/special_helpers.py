from flask import session
from flask_login import current_user
from app.db.db import db
from app.utils.model_helpers import kw_get_models, get_all_models, kw_get_model, kw_update_model
from app.models.spell import Spell
from app.models.slots import Slots


def get_filtered_spells(filter):
    # check if the url parameter is a valid class
    # if it is, get the list of spells that are available to that class
    # otherwise, just get a list of all spells
    if filter == 'Bard':
        spells = kw_get_models(Spell, is_bard=1)
    elif filter == 'Cleric':
        spells = kw_get_models(Spell, is_cleric=1)
    elif filter == 'Druid':
        spells = kw_get_models(Spell, is_druid=1)
    elif filter == 'Paladin':
        spells = kw_get_models(Spell, is_paladin=1)
    elif filter == 'Ranger':
        spells = kw_get_models(Spell, is_ranger=1)
    elif filter == 'Sorcerer':
        spells = kw_get_models(Spell, is_sorcerer=1)
    elif filter == 'Warlock':
        spells = kw_get_models(Spell, is_warlock=1)
    elif filter == 'Wizard':
        spells = kw_get_models(Spell, is_wizard=1)
    else:
        spells = get_all_models(Spell)

    # Find the class model associated with the filter
    return spells


def toggle_prepared_sb(sb):
    obj.query.filter_by(id=sb.id).update({'prepared': not sb.prepared})
    db.session.commit()


def reset_slots(char):
    slots = kw_get_model(Slots, char_id=char.id)
    vals = get_slots(char.level)
    updates = {}
    for i in range(0, 9):
        lvl = 'lvl_{}'.format(i+1)
        res = vals[i]
        updates.update({lvl:res})

    kw_update_model(slots, updates, char_id=char.id)

def get_slots(char_lvl):
    lvl = int(char_lvl)
    if lvl <= 1:
        return [2, 0, 0, 0, 0, 0, 0, 0, 0]

    if lvl == 2:
        return [3, 0, 0, 0, 0, 0, 0, 0, 0]

    if lvl == 3:
        return [4, 2, 0, 0, 0, 0, 0, 0, 0]

    if lvl == 4:
        return [4, 3, 0, 0, 0, 0, 0, 0, 0]

    if lvl == 5:
        return [4, 3, 2, 0, 0, 0, 0, 0, 0]

    if lvl == 6:
        return [4, 3, 3, 0, 0, 0, 0, 0, 0]

    if lvl == 7:
        return [4, 3, 3, 1, 0, 0, 0, 0, 0]

    if lvl == 8:
        return [4, 3, 3, 2, 0, 0, 0, 0, 0]

    if lvl == 9:
        return [4, 3, 3, 3, 1, 0, 0, 0, 0]

    if lvl == 10:
        return [4, 3, 3, 3, 2, 0, 0, 0, 0]

    if lvl == 11:
        return [4, 3, 3, 3, 2, 1, 0, 0, 0]

    if lvl == 12:
        return [4, 3, 3, 3, 2, 1, 0, 0, 0]

    if lvl == 13:
        return [4, 3, 3, 3, 2, 1, 1, 0, 0]

    if lvl == 14:
        return [4, 3, 3, 3, 2, 1, 1, 0, 0]

    if lvl == 15:
        return [4, 3, 3, 3, 2, 1, 1, 1, 0]

    if lvl == 16:
        return [4, 3, 3, 3, 2, 1, 1, 1, 0]

    if lvl == 17:
        return [4, 3, 3, 3, 2, 1, 1, 1, 1]

    if lvl == 18:
        return [4, 3, 3, 3, 3, 1, 1, 1, 1]

    if lvl == 19:
        return [4, 3, 3, 3, 3, 2, 1, 1, 1]

    if lvl >= 20:
        return [4, 3, 3, 3, 3, 2, 2, 1, 1]

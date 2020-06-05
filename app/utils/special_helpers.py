from flask import session
from flask_login import current_user
from app.db.db import db
from app.utils.model_helpers import kw_get_models, get_all_models, kw_get_model
from app.models.spell import Spell

def get_filtered_spells(filter):
    # check if the url parameter is a valid class
    # if it is, get the list of spells that are available to that class
    # otherwise, just get a list of all spells
    if filter== 'Bard':
        spells = kw_get_models(Spell, is_bard=1)
    elif filter== 'Cleric':
        spells = kw_get_models(Spell, is_cleric=1)
    elif filter== 'Druid':
        spells = kw_get_models(Spell, is_druid=1)
    elif filter== 'Paladin':
        spells = kw_get_models(Spell, is_paladin=1)
    elif filter== 'Ranger':
        spells = kw_get_models(Spell, is_ranger=1)
    elif filter== 'Sorcerer':
        spells = kw_get_models(Spell, is_sorcerer=1)
    elif filter== 'Warlock':
        spells = kw_get_models(Spell, is_warlock=1)
    elif filter== 'Wizard':
        spells = kw_get_models(Spell, is_wizard=1)
    else:
        spells = get_all_models(Spell)

    # Find the class model associated with the filter
    return spells